import { screen, waitFor, within } from '@testing-library/react'
import { afterEach, expect, test, vi } from 'vitest'
import { api } from '../api/client'
import { renderApp } from '../test/render'

afterEach(() => {
  vi.restoreAllMocks()
})

const ok = (data: unknown, status = 200) => ({ data, response: new Response(null, { status }) }) as never
const note = { id: 1, title: 'Sprint', body: 'Great review.', created_at: '2026-10-01T09:00:00Z', sentiment: 'positive' as const }

test('redirects / to the notes page and lists notes', async () => {
  vi.spyOn(api, 'GET').mockResolvedValue(ok([note]))
  renderApp('/')
  expect(await screen.findByRole('heading', { name: 'Notes (1)' })).toBeTruthy()
  expect(screen.getByText('Sprint')).toBeTruthy()
})

test('new note dialog shows Zod errors and does not post', async () => {
  vi.spyOn(api, 'GET').mockResolvedValue(ok([]))
  const post = vi.spyOn(api, 'POST')
  const { user } = renderApp('/notes')
  await user.click(await screen.findByRole('button', { name: 'New note' }))
  const dialog = screen.getByRole('dialog', { name: 'New note' })
  await user.click(within(dialog).getByRole('button', { name: 'Add' }))
  expect(await within(dialog).findByText('Title is required')).toBeTruthy()
  expect(within(dialog).getByText('Body is required')).toBeTruthy()
  expect(post).not.toHaveBeenCalled()
})

test('creating a note posts, toasts, closes the dialog and refetches the list', async () => {
  const get = vi.spyOn(api, 'GET').mockResolvedValueOnce(ok([])).mockResolvedValue(ok([note]))
  const post = vi.spyOn(api, 'POST').mockResolvedValue(ok(note, 201))
  const { user } = renderApp('/notes')
  await user.click(await screen.findByRole('button', { name: 'New note' }))
  const dialog = screen.getByRole('dialog', { name: 'New note' })
  await user.type(within(dialog).getByRole('textbox', { name: /title/i }), 'Sprint')
  await user.type(within(dialog).getByRole('textbox', { name: /body/i }), 'Great review.')
  await user.click(within(dialog).getByRole('button', { name: 'Add' }))

  expect(await screen.findByText('Note added')).toBeTruthy()
  expect(post).toHaveBeenCalledWith('/api/notes', { body: { title: 'Sprint', body: 'Great review.' } })
  await waitFor(() => expect(screen.queryByRole('dialog')).toBeNull())
  expect(await screen.findByRole('heading', { name: 'Notes (1)' })).toBeTruthy()
  expect(get).toHaveBeenCalledTimes(2)
})

test('shows an error with retry when the list fails to load', async () => {
  vi.spyOn(api, 'GET').mockResolvedValue({ error: { detail: 'x' }, response: new Response(null, { status: 500 }) } as never)
  renderApp('/notes')
  expect(await screen.findByText('Request failed (500)')).toBeTruthy()
  expect(screen.getByRole('button', { name: 'Retry' })).toBeTruthy()
})

test('unknown routes show the not-found page', async () => {
  renderApp('/nope')
  expect(await screen.findByRole('heading', { name: 'Page not found' })).toBeTruthy()
})
