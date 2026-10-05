import { expect, test } from 'vitest'
import { filterNotes } from './notesFilterSlice'

const n = (id: number, created_at: string, sentiment: 'positive' | 'negative' | null = null) => ({ id, title: '', body: '', created_at, sentiment })

test('filters by date (inclusive) and sentiment', () => {
  const notes = [n(1, '2026-09-30T23:00:00Z', 'positive'), n(2, '2026-10-01T08:00:00Z', 'negative'), n(3, '2026-10-02T08:00:00Z', 'positive')]
  expect(filterNotes(notes, { since: null, sentiment: null }).map((x) => x.id)).toEqual([1, 2, 3])
  expect(filterNotes(notes, { since: '2026-10-01', sentiment: null }).map((x) => x.id)).toEqual([2, 3])
  expect(filterNotes(notes, { since: '2026-10-01', sentiment: 'positive' }).map((x) => x.id)).toEqual([3])
})
