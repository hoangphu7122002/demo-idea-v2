import type { ChipProps } from '@mui/material/Chip'
import type { Sentiment } from './notesFilterSlice'

/** One place for how each sentiment looks; chips and selects both read from it. */
export const SENTIMENT_META: Record<Sentiment, { label: string; color: ChipProps['color'] }> = {
  positive: { label: 'Positive', color: 'success' },
  neutral: { label: 'Neutral', color: 'default' },
  negative: { label: 'Negative', color: 'error' },
}

export const SENTIMENT_OPTIONS = (Object.keys(SENTIMENT_META) as Sentiment[]).map((s) => ({ value: s, label: SENTIMENT_META[s].label }))
