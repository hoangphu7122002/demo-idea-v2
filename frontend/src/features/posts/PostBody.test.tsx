import { describe, expect, it } from 'vitest'
import { renderWithProviders } from '../../test/render'
import PostBody from './PostBody'

const paragraphs = [
  { id: 'p-intro', md: 'Hello **world** with a [link](https://example.com).' },
  { id: 'p-code', md: '```python\ndef f(x):\n    return x + 1\n```' },
  { id: 'p-math', md: 'Euler: $e^{i\\pi} + 1 = 0$' },
  { id: 'p-table', md: '| a | b |\n|---|---|\n| 1 | 2 |' },
]

describe('PostBody', () => {
  it('renders each block in a section whose id is the paragraph id', () => {
    const { container } = renderWithProviders(<PostBody paragraphs={paragraphs} />)
    const sections = container.querySelectorAll('section')
    expect(Array.from(sections).map((s) => s.id)).toEqual(paragraphs.map((p) => p.id))
    sections.forEach((s) => expect(s.dataset.paragraphId).toBe(s.id))
    expect(container.querySelector('#p-intro strong')?.textContent).toBe('world')
  })

  it('highlights code, renders math and gfm tables', () => {
    const { container } = renderWithProviders(<PostBody paragraphs={paragraphs} />)
    const code = container.querySelector('#p-code pre code')
    expect(code?.className).toContain('hljs')
    expect(code?.querySelector('.hljs-keyword')).not.toBeNull()
    expect(container.querySelector('#p-math .katex')).not.toBeNull()
    expect(container.querySelectorAll('#p-table td')).toHaveLength(2)
  })

  it('does not render raw HTML or javascript: links (XSS)', () => {
    const evil = [
      { id: 'x-1', md: 'before <script>window.__xss = 1</script> after' },
      { id: 'x-2', md: '<img src="x" onerror="window.__xss = 1"> text' },
      { id: 'x-3', md: '[click](javascript:window.__xss=1)' },
    ]
    const { container } = renderWithProviders(<PostBody paragraphs={evil} />)
    expect(container.querySelector('script')).toBeNull()
    expect(container.querySelector('img')).toBeNull()
    expect(container.querySelector('[onerror]')).toBeNull()
    const a = container.querySelector('#x-3 a')
    expect(a?.getAttribute('href') ?? '').not.toMatch(/^javascript:/i)
    expect((window as unknown as { __xss?: number }).__xss).toBeUndefined()
  })
})
