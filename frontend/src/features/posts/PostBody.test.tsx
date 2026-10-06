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
      { id: 'x-3', md: '[click me](javascript:window.__xss=1)' },
    ]
    const { container } = renderWithProviders(<PostBody paragraphs={evil} />)
    // Raw HTML is shown as inert text (fails if raw HTML were parsed into elements).
    expect(container.querySelector('#x-1')?.textContent).toContain('<script>window.__xss = 1</script>')
    expect(container.querySelector('#x-2')?.textContent).toContain('<img src="x" onerror="window.__xss = 1">')
    expect(container.querySelector('script')).toBeNull()
    expect(container.querySelector('img')).toBeNull()
    // The link text still renders, but without a javascript: href (fails if urlTransform is disabled).
    const link = Array.from(container.querySelectorAll('#x-3 a')).find((a) => a.textContent === 'click me')
    expect(link).toBeDefined()
    expect(link?.getAttribute('href') ?? '').not.toMatch(/^javascript:/i)
    expect((window as unknown as { __xss?: number }).__xss).toBeUndefined()
  })

  it('themes links and marks flagged paragraphs', () => {
    const { container } = renderWithProviders(
      <PostBody paragraphs={[{ id: 'a', md: '[docs](https://example.com)' }, { id: 'b', md: 'plain' }]} flaggedIds={['b']} />,
    )
    const link = container.querySelector('#a a') as HTMLElement
    expect(link.getAttribute('href')).toBe('https://example.com')
    const color = getComputedStyle(link).color
    expect(color).not.toBe('')
    expect(color).not.toBe(getComputedStyle(container.querySelector('#b') as HTMLElement).color)
    expect(container.querySelector('#b')?.hasAttribute('data-flagged')).toBe(true)
    expect(container.querySelector('#a')?.hasAttribute('data-flagged')).toBe(false)
  })
})
