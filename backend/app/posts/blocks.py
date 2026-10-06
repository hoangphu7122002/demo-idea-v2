"""Split markdown into top-level blocks (one block = one commentable paragraph)."""

import re

_FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
_HEADING = re.compile(r"^\s{0,3}#{1,6}(\s|$)")
_LIST = re.compile(r"^\s{0,3}([-*+]|\d+[.)])\s")
_QUOTE = re.compile(r"^\s{0,3}>")


def _kind(line: str) -> str:
    if _LIST.match(line):
        return "list"
    if _QUOTE.match(line):
        return "quote"
    return "para"


def split_blocks(md: str) -> list[str]:
    lines = md.replace("\r\n", "\n").split("\n")
    blocks: list[list[str]] = []
    cur: list[str] = []
    cur_kind = ""

    def flush() -> None:
        nonlocal cur, cur_kind
        if cur:
            blocks.append(cur)
        cur, cur_kind = [], ""

    i = 0
    while i < len(lines):
        line = lines[i]
        fence = _FENCE.match(line)
        if fence:  # fenced code: whole, blank lines included, wins over math
            flush()
            marker = fence.group(1)
            block = [line]
            i += 1
            while i < len(lines):
                block.append(lines[i])
                closing = lines[i].strip()
                i += 1
                if closing.startswith(marker[0] * len(marker)) and set(closing) == {marker[0]}:
                    break
            blocks.append(block)
            continue
        if line.strip().startswith("$$"):  # math: whole until closing $$
            flush()
            block = [line]
            rest = line.strip()[2:]
            i += 1
            if "$$" not in rest:
                while i < len(lines):
                    block.append(lines[i])
                    done = "$$" in lines[i]
                    i += 1
                    if done:
                        break
            blocks.append(block)
            continue
        if not line.strip():
            flush()
        elif _HEADING.match(line):
            flush()
            blocks.append([line])
        else:
            kind = _kind(line)
            # lazy continuation (indented / plain text) stays in a list or quote
            if cur and kind == "para" and cur_kind in {"list", "quote"}:
                cur.append(line)
            else:
                if cur and kind != cur_kind:
                    flush()
                cur.append(line)
                cur_kind = kind
        i += 1
    flush()
    return ["\n".join(b).strip("\n") for b in blocks]
