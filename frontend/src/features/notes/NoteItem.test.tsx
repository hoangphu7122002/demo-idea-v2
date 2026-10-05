import { screen } from '@testing-library/react'
import { afterEach, expect, test, vi } from 'vitest'
import { renderWithProviders } from '../../test/render'
import { NoteItem } from './NoteItem'
import * as summary from './summary'

afterEach(() => {
  vi.restoreAllMocks()
})

const note = { id: 1, title: 'Sprint', body: 'Great review.', created_at: '2026-10-03T00:00:00Z' }

test('shows pending state, then toasts when the summary is ready', async () => {
  let finish: () => void = () => {}
  vi.spyOn(summary, 'summariseNote').mockReturnValue(new Promise<void>((r) => (finish = r)))
  const { user } = renderWithProviders(<NoteItem note={note} />)
  await user.click(screen.getByRole('button', { name: 'Summarise' }))
  expect(await screen.findByRole('button', { name: /Summarising/ })).toHaveProperty('disabled', true)
  finish()
  expect(await screen.findByText('Summary ready')).toBeTruthy()
  expect(await screen.findByRole('button', { name: 'Summarise' })).toHaveProperty('disabled', false)
})

test('renders summary chips and an inline error', async () => {
  vi.spyOn(summary, 'summariseNote').mockRejectedValue(new Error('Summary failed'))
  const { user } = renderWithProviders(<NoteItem note={{ ...note, summary: 'Great review.', tags: ['sprint', 'review'], sentiment: 'positive' }} />)
  expect(screen.getByText('sprint')).toBeTruthy()
  expect(screen.getByText('Positive')).toBeTruthy()
  await user.click(screen.getByRole('button', { name: 'Summarise' }))
  expect((await screen.findByRole('alert')).textContent).toBe('Summary failed')
})
