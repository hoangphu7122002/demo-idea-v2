import { zodResolver } from '@hookform/resolvers/zod'
import { useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { FormDialog } from '../../components/FormDialog'
import { FormTextField } from '../../components/form/FormTextField'
import { useMutationToast } from '../../hooks/useMutationToast'
import { useCreateNoteMutation } from './notesApi'
import { noteFormSchema, type NoteFormValues } from './noteSchema'

const EMPTY: NoteFormValues = { title: '', body: '' }

export function NoteFormDialog({ open, onClose }: { open: boolean; onClose: () => void }) {
  const [createNote] = useCreateNoteMutation()
  const run = useMutationToast()
  const { control, handleSubmit, reset, formState } = useForm<NoteFormValues>({
    resolver: zodResolver(noteFormSchema),
    defaultValues: EMPTY,
  })

  useEffect(() => {
    if (open) reset(EMPTY)
  }, [open, reset])

  const onSubmit = handleSubmit(async (values) => {
    if (await run(createNote(values).unwrap(), { success: 'Note added', error: 'Could not add note' })) onClose()
  })

  return (
    <FormDialog open={open} title="New note" onClose={onClose} onSubmit={onSubmit} submitLabel="Add" submitting={formState.isSubmitting}>
      <FormTextField control={control} name="title" label="Title" required autoFocus />
      <FormTextField control={control} name="body" label="Body" required multiline minRows={3} />
    </FormDialog>
  )
}
