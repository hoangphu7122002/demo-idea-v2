import Box from '@mui/material/Box'
import 'katex/dist/katex.min.css'
import ReactMarkdown from 'react-markdown'
import rehypeHighlight from 'rehype-highlight'
import rehypeKatex from 'rehype-katex'
import remarkGfm from 'remark-gfm'
import remarkMath from 'remark-math'

export interface PostParagraph {
  id: string
  md: string
}

const remarkPlugins = [remarkGfm, remarkMath]
const rehypePlugins = [rehypeKatex, rehypeHighlight]

/** highlight.js token colours from palette tokens, so light and dark both work. */
const hljsTheme = {
  '& .hljs-comment, & .hljs-quote': { color: 'text.secondary', fontStyle: 'italic' },
  '& .hljs-keyword, & .hljs-selector-tag, & .hljs-literal': { color: 'primary.main' },
  '& .hljs-string, & .hljs-regexp, & .hljs-addition': { color: 'success.main' },
  '& .hljs-number, & .hljs-symbol, & .hljs-bullet': { color: 'warning.main' },
  '& .hljs-title, & .hljs-section, & .hljs-built_in, & .hljs-type': { color: 'secondary.main' },
  '& .hljs-attr, & .hljs-attribute, & .hljs-variable, & .hljs-name': { color: 'info.main' },
  '& .hljs-deletion': { color: 'error.main' },
}

/** Renders post paragraphs (markdown + code + math). Each block is a section whose id is the paragraph id. */
export default function PostBody({ paragraphs }: { paragraphs: PostParagraph[] }) {
  return (
    <Box
      sx={{
        maxWidth: 720,
        mx: 'auto',
        fontSize: 18,
        lineHeight: 1.7,
        color: 'text.primary',
        overflowWrap: 'anywhere',
        '& img': { maxWidth: '100%' },
        '& pre': {
          p: 2,
          overflowX: 'auto',
          bgcolor: 'background.paper',
          border: 1,
          borderColor: 'divider',
          borderRadius: 1,
          fontSize: 15,
          lineHeight: 1.5,
        },
        '& code': { fontFamily: 'ui-monospace, SFMono-Regular, Menlo, monospace' },
        '& :not(pre) > code': { px: 0.5, bgcolor: 'action.hover', borderRadius: 0.5, fontSize: '0.9em' },
        '& table': { borderCollapse: 'collapse' },
        '& th, & td': { border: 1, borderColor: 'divider', px: 1, py: 0.5 },
        '& blockquote': { m: 0, pl: 2, borderLeft: 3, borderColor: 'divider', color: 'text.secondary' },
        ...hljsTheme,
      }}
    >
      {paragraphs.map((p) => (
        <Box component="section" key={p.id} id={p.id} data-paragraph-id={p.id} sx={{ my: 2 }}>
          <ReactMarkdown remarkPlugins={remarkPlugins} rehypePlugins={rehypePlugins}>
            {p.md}
          </ReactMarkdown>
        </Box>
      ))}
    </Box>
  )
}
