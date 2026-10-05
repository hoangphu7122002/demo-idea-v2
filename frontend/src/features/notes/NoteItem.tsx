import Alert from '@mui/material/Alert'
import Button from '@mui/material/Button'
import Chip from '@mui/material/Chip'
import Paper from '@mui/material/Paper'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import dayjs from 'dayjs'
import { useSnackbar } from 'notistack'
import { useState } from 'react'
import { SENTIMENT_META } from './noteMeta'
import { useSummariseNoteMutation, type Note } from './notesApi'

export function NoteItem({ note }: { note: Note }) {
  const [summarise, { isLoading }] = useSummariseNoteMutation()
  const { enqueueSnackbar } = useSnackbar()
  const [error, setError] = useState<string | null>(null)

  async function onSummarise() {
    setError(null)
    try {
      await summarise(note.id).unwrap()
      enqueueSnackbar('Summary ready', { variant: 'success' })
    } catch (e) {
      // Shown inline: the error belongs to this note, not to the page.
      setError(e && typeof e === 'object' && 'message' in e ? String(e.message) : 'Summary failed')
    }
  }

  return (
    <Paper component="li" sx={{ p: 2 }}>
      <Stack spacing={1}>
        <Stack direction="row" spacing={2} sx={{ alignItems: 'center', justifyContent: 'space-between' }}>
          <Typography variant="subtitle1" sx={{ fontWeight: 700 }}>
            {note.title}
          </Typography>
          <Button size="small" variant="outlined" onClick={onSummarise} loading={isLoading} loadingPosition="start">
            {isLoading ? 'Summarising…' : 'Summarise'}
          </Button>
        </Stack>
        <Typography>{note.body}</Typography>
        <Typography variant="caption" color="text.secondary">
          {dayjs(note.created_at).format('D MMM YYYY, HH:mm')}
        </Typography>
        {error && <Alert severity="error">{error}</Alert>}
        {note.summary && (
          <Stack spacing={1}>
            <Typography sx={{ fontStyle: 'italic' }}>{note.summary}</Typography>
            <Stack direction="row" spacing={0.5} useFlexGap sx={{ flexWrap: 'wrap' }}>
              {note.sentiment && <Chip label={SENTIMENT_META[note.sentiment].label} color={SENTIMENT_META[note.sentiment].color} />}
              {note.tags?.map((t) => <Chip key={t} label={t} variant="outlined" />)}
            </Stack>
          </Stack>
        )}
      </Stack>
    </Paper>
  )
}
