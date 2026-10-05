import Button from '@mui/material/Button'
import MenuItem from '@mui/material/MenuItem'
import Stack from '@mui/material/Stack'
import TextField from '@mui/material/TextField'
import { DatePicker } from '@mui/x-date-pickers/DatePicker'
import dayjs from 'dayjs'
import { useAppDispatch, useAppSelector } from '../../app/hooks'
import { SENTIMENT_OPTIONS } from './noteMeta'
import { clearFilter, setSentiment, setSince, type Sentiment } from './notesFilterSlice'

export function NotesFilterBar() {
  const dispatch = useAppDispatch()
  const { since, sentiment } = useAppSelector((s) => s.notesFilter)
  return (
    <Stack direction={{ xs: 'column', sm: 'row' }} spacing={1.5} sx={{ mb: 2 }}>
      <DatePicker
        label="Since"
        value={since ? dayjs(since) : null}
        onChange={(d) => dispatch(setSince(d && d.isValid() ? d.format('YYYY-MM-DD') : null))}
        disableFuture
        slotProps={{ textField: { size: 'small' } }}
      />
      <TextField
        select
        label="Sentiment"
        value={sentiment ?? ''}
        onChange={(e) => dispatch(setSentiment((e.target.value || null) as Sentiment | null))}
        sx={{ minWidth: 160 }}
      >
        <MenuItem value="">
          <em>Any</em>
        </MenuItem>
        {SENTIMENT_OPTIONS.map((o) => (
          <MenuItem key={o.value} value={o.value}>
            {o.label}
          </MenuItem>
        ))}
      </TextField>
      {(since || sentiment) && <Button onClick={() => dispatch(clearFilter())}>Clear</Button>}
    </Stack>
  )
}
