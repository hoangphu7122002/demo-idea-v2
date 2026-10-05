import AddIcon from '@mui/icons-material/Add'
import Button from '@mui/material/Button'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import { useState } from 'react'
import { useAppSelector } from '../app/hooks'
import { PageHeader } from '../components/PageHeader'
import { QueryState } from '../components/QueryState'
import { NoteFormDialog } from '../features/notes/NoteFormDialog'
import { NoteItem } from '../features/notes/NoteItem'
import { useGetNotesQuery } from '../features/notes/notesApi'
import { filterNotes } from '../features/notes/notesFilterSlice'
import { NotesFilterBar } from '../features/notes/NotesFilterBar'

export function NotesPage() {
  const notesQuery = useGetNotesQuery()
  const filter = useAppSelector((s) => s.notesFilter)
  const [creating, setCreating] = useState(false)

  return (
    <>
      <PageHeader
        title={`Notes (${notesQuery.data?.length ?? 0})`}
        actions={
          <Button variant="contained" startIcon={<AddIcon />} onClick={() => setCreating(true)}>
            New note
          </Button>
        }
      />
      <NotesFilterBar />
      <QueryState query={notesQuery} emptyMessage="No notes yet. Add one to try the AI summary.">
        {(notes) => {
          const visible = filterNotes(notes, filter)
          if (visible.length === 0) {
            return (
              <Typography color="text.secondary" sx={{ textAlign: 'center', py: 6 }}>
                No notes match the filter.
              </Typography>
            )
          }
          return (
            <Stack component="ul" spacing={1.5} sx={{ listStyle: 'none', m: 0, p: 0 }}>
              {visible.map((n) => (
                <NoteItem key={n.id} note={n} />
              ))}
            </Stack>
          )
        }}
      </QueryState>
      <NoteFormDialog open={creating} onClose={() => setCreating(false)} />
    </>
  )
}
