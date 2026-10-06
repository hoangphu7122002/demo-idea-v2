# Calling the Claude API from Python

This post walks through the basics of calling a large language model from Python: installing the SDK, sending a first message, streaming, and reasoning about cost.

## Install and authenticate

Install the official Anthropic SDK and export your API key. The client reads `ANTHROPIC_API_KEY` from the environment, so no secret ends up in source control.

```bash
pip install anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Your first message

A request needs a model name, a token limit and a list of messages. Here we use `claude-sonnet-4-5`, a good default for most tasks.

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain tokens in one paragraph."}],
)

print(message.content[0].text)
```

The response holds a list of content blocks. For plain text replies the first block carries the answer.

## Streaming

Long answers feel faster when you stream them. The SDK exposes a context manager that yields text deltas as they arrive.

```python
with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a haiku about latency."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

Things to keep in mind when streaming:

- Handle network errors and retry from the last complete message.
- Flush output so the user sees tokens immediately.
- Stop reading when the stream context closes.

## Estimating cost

Pricing is per token, split between input and output. With input price $p_{in}$ and output price $p_{out}$ per million tokens, one request costs:

$$
\text{cost} = \frac{n_{in} \cdot p_{in} + n_{out} \cdot p_{out}}{10^6}
$$

Output tokens usually cost several times more than input tokens, so capping `max_tokens` is the cheapest guard against surprise bills.

> Measure real token counts from the `usage` field of each response instead of guessing from word counts.

## Wrap up

You now know how to install the SDK, send a message, stream a reply and estimate cost. Next step: add a system prompt and structured output.
