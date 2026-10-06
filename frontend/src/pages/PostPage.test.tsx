import { screen } from '@testing-library/react'
import { afterEach, expect, test, vi } from 'vitest'
import { api } from '../api/client'
import { renderApp } from '../test/render'

afterEach(() => {
  vi.restoreAllMocks()
})

test('renders the post title and paragraphs with ids', async () => {
  vi.spyOn(api, 'GET').mockResolvedValue({
    data: { slug: 's', title: 'Hello post', paragraphs: [{ id: 'p-1', md: 'First **para**' }, { id: 'p-2', md: 'Second' }] },
    response: new Response(null, { status: 200 }),
  } as never)
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
