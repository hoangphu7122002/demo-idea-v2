import { createSlice, type PayloadAction } from '@reduxjs/toolkit'
import type { Note } from './notesApi'

export type Sentiment = NonNullable<Note['sentiment']>

export interface NotesFilter {
  /** ISO date (`YYYY-MM-DD`); show notes created on or after it. */
  since: string | null
  sentiment: Sentiment | null
}

const initialState: NotesFilter = { since: null, sentiment: null }

/** Client-only UI state, kept in Redux so it survives navigating away and back. Server data stays in RTK Query. */
export const notesFilterSlice = createSlice({
  name: 'notesFilter',
  initialState,
  reducers: {
    setSince: (state, action: PayloadAction<string | null>) => {
      state.since = action.payload
    },
    setSentiment: (state, action: PayloadAction<Sentiment | null>) => {
      state.sentiment = action.payload
    },
    clearFilter: () => initialState,
  },
})

export const { setSince, setSentiment, clearFilter } = notesFilterSlice.actions

export function filterNotes(notes: Note[], { since, sentiment }: NotesFilter): Note[] {
  return notes.filter((n) => (!since || n.created_at.slice(0, 10) >= since) && (!sentiment || n.sentiment === sentiment))
}
