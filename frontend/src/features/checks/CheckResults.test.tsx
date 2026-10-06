import { screen } from '@testing-library/react'
import { expect, test, vi } from 'vitest'
import { renderWithProviders } from '../../test/render'
import { CheckResults } from './CheckResults'
import type { Flag } from './types'

const flags: Flag[] = [
  { paragraph_id: 'p-3', reason: 'Model name retired', source_quote: 'claude-x is removed', proposed_fix: 'Use claude-y' },
  { paragraph_id: 'p-7', reason: 'Param renamed', source_quote: 'max_tokens is now required', proposed_fix: 'Pass max_tokens' },
]

test('renders each flag with link, reason, quote and fix', () => {
  renderWithProviders(<CheckResults flags={flags} />)
  expect(screen.getAllByRole('listitem')).toHaveLength(2)
  expect(screen.getByRole('link', { name: '#p-3' }).getAttribute('href')).toBe('#p-3')
  expect(screen.getByText('Model name retired')).toBeTruthy()
  expect(screen.getByText('claude-x is removed')).toBeTruthy()
  expect(screen.getByText(/Use claude-y/)).toBeTruthy()
  expect(screen.queryByText('Cached result')).toBeNull()
})

test('empty state', () => {
  renderWithProviders(<CheckResults flags={[]} />)
  expect(screen.getByText('No outdated paragraphs found.')).toBeTruthy()
})

test('cache note and onSelect', async () => {
  const onSelect = vi.fn()
  const { user } = renderWithProviders(<CheckResults flags={flags} source="cache" onSelect={onSelect} />)
  expect(screen.getByText('Cached result')).toBeTruthy()
  await user.click(screen.getByRole('link', { name: '#p-7' }))
  expect(onSelect).toHaveBeenCalledWith('p-7')
})
