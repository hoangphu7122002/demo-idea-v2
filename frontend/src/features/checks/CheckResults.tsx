import Alert from '@mui/material/Alert'
import Box from '@mui/material/Box'
import Link from '@mui/material/Link'
import Paper from '@mui/material/Paper'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import type { CheckSource, Flag } from './checksApi'

interface CheckResultsProps {
  flags: Flag[]
  source?: CheckSource | null
  /** Called when a flag's paragraph link is clicked (the default hash navigation still runs). */
  onSelect?: (paragraphId: string) => void
}

/** Flagged paragraphs: link to the paragraph, why it is outdated, the resource quote and the proposed fix. */
export function CheckResults({ flags, source, onSelect }: CheckResultsProps) {
  return (
    <Stack spacing={2}>
      {source === 'cache' && <Typography variant="caption" color="text.secondary">Cached result</Typography>}
      {flags.length === 0 ? (
        <Alert severity="success">No outdated paragraphs found.</Alert>
      ) : (
        <Stack component="ul" spacing={2} sx={{ listStyle: 'none', p: 0, m: 0 }} aria-label="Flagged paragraphs">
          {flags.map((f, i) => (
            <Paper component="li" key={`${f.paragraph_id}-${i}`} variant="outlined" sx={{ p: 2 }}>
              <Link href={`#${f.paragraph_id}`} onClick={() => onSelect?.(f.paragraph_id)} sx={{ fontWeight: 700 }}>
                #{f.paragraph_id}
              </Link>
              <Typography sx={{ mt: 1 }}>{f.reason}</Typography>
              <Box component="blockquote" sx={{ m: 0, my: 1, pl: 2, borderLeft: 3, borderColor: 'divider', color: 'text.secondary' }}>
                {f.source_quote}
              </Box>
              <Typography variant="body2">
                <strong>Proposed fix:</strong> {f.proposed_fix}
              </Typography>
            </Paper>
          ))}
        </Stack>
      )}
    </Stack>
  )
}
