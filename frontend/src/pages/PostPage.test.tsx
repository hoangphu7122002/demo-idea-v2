import { screen, waitFor } from '@testing-library/react'
import { afterEach, expect, test, vi } from 'vitest'
import { api } from '../api/client'
import { renderApp } from '../test/render'

const originalScrollIntoView = window.HTMLElement.prototype.scrollIntoView

afterEach(() => {
  vi.restoreAllMocks()
  window.HTMLElement.prototype.scrollIntoView = originalScrollIntoView
})

test('renders the post title and paragraphs with ids', async () => {
  vi.spyOn(api, 'GET').mockImplementation(((path: string) =>
    Promise.resolve({
      data: path.endsWith('/flags')
        ? null
        : { slug: 's', title: 'Hello post', paragraphs: [{ id: 'p-1', md: 'First **para**' }, { id: 'p-2', md: 'Second' }] },
      response: new Response(null, { status: 200 }),
    })) as never)
  const { container } = renderApp('/posts/s')
  expect(await screen.findByRole('heading', { name: 'Hello post' })).toBeTruthy()
  expect(container.querySelector('section#p-1 strong')?.textContent).toBe('para')
  expect(container.querySelector('section#p-2')).not.toBeNull()
})

test('unknown slug shows the not-found state', async () => {
  vi.spyOn(api, 'GET').mockResolvedValue({ error: { detail: 'Not Found' }, response: new Response(null, { status: 404 }) } as never)
  renderApp('/posts/nope')
  expect(await screen.findByRole('heading', { name: 'Page not found' })).toBeTruthy()
})

const post = {
  slug: 's',
  title: 'Hello post',
  paragraphs: [{ id: 'p-1', md: 'one' }, { id: 'p-2', md: 'two' }, { id: 'p-3', md: 'three' }],
}
const flag = (id: string, reason: string) => ({ paragraph_id: id, reason, source_quote: 'quote', proposed_fix: 'fix' })
const res = (data: unknown, status = 200) => ({ data, response: new Response(null, { status }) }) as never
const fail = (error: unknown, status: number) => ({ error, response: new Response(null, { status }) }) as never

function mockApi({ flags = null as unknown, check }: { flags?: unknown; check?: unknown }) {
  vi.spyOn(api, 'GET').mockImplementation(((path: string) => Promise.resolve(path.endsWith('/flags') ? res(flags) : res(post))) as never)
  return vi.spyOn(api, 'POST').mockResolvedValue(check as never)
}

test('check posts the URL, lists flags, marks paragraphs and notes a cached result', async () => {
  const flags = [flag('p-2', 'Outdated model'), flag('p-3', 'Renamed param')]
  const post_ = mockApi({ check: res({ check_id: 1, source: 'cache', resource_url: 'https://x.test/r', flags }) })
  const { container, user } = renderApp('/posts/s')
  await user.type(await screen.findByLabelText('Resource URL'), 'https://x.test/r')
  await user.click(screen.getByRole('button', { name: 'Check' }))
  expect(await screen.findByText('Outdated model')).toBeTruthy()
  expect(post_).toHaveBeenCalledWith('/api/posts/{slug}/check', { params: { path: { slug: 's' } }, body: { resource_url: 'https://x.test/r' } })
  expect(screen.getByText('Cached result')).toBeTruthy()
  expect(container.querySelector('#p-2')?.hasAttribute('data-flagged')).toBe(true)
  expect(container.querySelector('#p-1')?.hasAttribute('data-flagged')).toBe(false)
})

test('shows the latest stored flags on load (GET) without a source note', async () => {
  mockApi({ flags: { check_id: 1, source: null, resource_url: null, flags: [flag('p-1', 'Stored flag')] } })
  renderApp('/posts/s')
  expect(await screen.findByText('Stored flag')).toBeTruthy()
  expect(screen.queryByText('Cached result')).toBeNull()
})

test('clicking a flag scrolls to its paragraph', async () => {
  mockApi({ flags: { check_id: 1, source: null, resource_url: null, flags: [flag('p-3', 'Scroll me')] } })
  const scroll = vi.fn()
  window.HTMLElement.prototype.scrollIntoView = scroll
  const { user } = renderApp('/posts/s')
  await user.click(await screen.findByRole('link', { name: '#p-3' }))
  expect(scroll).toHaveBeenCalled()
  expect(scroll.mock.contexts[0]).toBe(document.getElementById('p-3'))
})

test('422 shows the server detail', async () => {
  mockApi({ check: fail({ detail: 'Unknown resource URL' }, 422) })
  const { user } = renderApp('/posts/s')
  await user.type(await screen.findByLabelText('Resource URL'), 'https://nope.test/x')
  await user.click(screen.getByRole('button', { name: 'Check' }))
  expect((await screen.findByRole('alert')).textContent).toContain('Unknown resource URL')
})

test('503 shows the unavailable message', async () => {
  mockApi({ check: fail({ detail: 'boom' }, 503) })
  const { user } = renderApp('/posts/s')
  await user.type(await screen.findByLabelText('Or paste resource text'), 'v2 changes')
  await user.click(screen.getByRole('button', { name: 'Check' }))
  await waitFor(() => expect(screen.getByRole('alert').textContent).toContain('Check unavailable, try again'))
})

test('switching posts does not show the previous post\'s check result', async () => {
  const other = { slug: 't', title: 'Other post', paragraphs: [{ id: 'p-1', md: 'other' }] }
  vi.spyOn(api, 'GET').mockImplementation(((path: string, init: { params: { path: { slug: string } } }) => {
    if (path.endsWith('/flags')) return Promise.resolve(res(null))
    return Promise.resolve(res(init.params.path.slug === 't' ? other : post))
  }) as never)
  vi.spyOn(api, 'POST').mockResolvedValue(
    res({ check_id: 1, source: 'live', resource_url: null, flags: [flag('p-2', 'Only for post s')] }),
  )
  const { router, user } = renderApp('/posts/s')
  await user.type(await screen.findByLabelText('Or paste resource text'), 'changes')
  await user.click(screen.getByRole('button', { name: 'Check' }))
  expect(await screen.findByText('Only for post s')).toBeTruthy()

  await router.navigate('/posts/t')
  expect(await screen.findByRole('heading', { name: 'Other post' })).toBeTruthy()
  expect(screen.queryByText('Only for post s')).toBeNull()
  expect((screen.getByLabelText('Or paste resource text') as HTMLTextAreaElement).value).toBe('')
})
