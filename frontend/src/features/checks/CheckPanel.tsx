import Alert from '@mui/material/Alert'
import Button from '@mui/material/Button'
import Stack from '@mui/material/Stack'
import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { FormTextField } from '../../components/form/FormTextField'
import { checkFormSchema, type CheckFormValues } from './checkSchema'
import type { CheckInput } from './types'

interface CheckPanelProps {
  onCheck: (input: CheckInput) => Promise<unknown>
  pending?: boolean
  error?: string
}

/** Form to check the post against a release: a URL or pasted text (at least one). */
export function CheckPanel({ onCheck, pending = false, error }: CheckPanelProps) {
  const { control, handleSubmit } = useForm<CheckFormValues>({
    resolver: zodResolver(checkFormSchema),
    defaultValues: { release_url: '', release_text: '' },
  })

  const onSubmit = handleSubmit(async (values) => {
    await onCheck({
      ...(values.release_url && { release_url: values.release_url }),
      ...(values.release_text && { release_text: values.release_text }),
    })
  })

  return (
    <Stack component="form" spacing={2} onSubmit={onSubmit} noValidate aria-label="Check against release">
      <FormTextField control={control} name="release_url" label="Release URL" disabled={pending} />
      <FormTextField control={control} name="release_text" label="Or paste release text" multiline minRows={3} disabled={pending} />
      {error && <Alert severity="error">{error}</Alert>}
      <Button type="submit" variant="contained" loading={pending} sx={{ alignSelf: 'flex-start' }}>
        Check
      </Button>
    </Stack>
  )
}
