import Alert from '@mui/material/Alert'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import { zodResolver } from '@hookform/resolvers/zod'
import { useForm } from 'react-hook-form'
import { FormTextField } from '../../components/form/FormTextField'
import { checkFormSchema, type CheckFormValues } from './checkSchema'
import type { CheckInput } from './checksApi'

interface CheckPanelProps {
  onCheck: (input: CheckInput) => Promise<unknown>
  pending?: boolean
  error?: string
}

/** Form to check the post against a resource (release note, docs page, changelog, paper…): a URL or pasted text (at least one). */
export function CheckPanel({ onCheck, pending = false, error }: CheckPanelProps) {
  const { control, handleSubmit } = useForm<CheckFormValues>({
    resolver: zodResolver(checkFormSchema),
    defaultValues: { resource_url: '', resource_text: '' },
  })

  const onSubmit = handleSubmit(async (values) => {
    await onCheck({
      ...(values.resource_url && { resource_url: values.resource_url }),
      ...(values.resource_text && { resource_text: values.resource_text }),
    })
  })

  return (
    <Stack component="form" spacing={2} onSubmit={onSubmit} noValidate aria-label="Check against a resource">
      <Box>
        <Typography variant="h6" component="h2">
          Check against a resource
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Paste a URL or text: a release note, docs page, changelog, paper…
        </Typography>
      </Box>
      <FormTextField control={control} name="resource_url" label="Resource URL" disabled={pending} />
      <FormTextField control={control} name="resource_text" label="Or paste resource text" multiline minRows={3} disabled={pending} />
      {error && <Alert severity="error">{error}</Alert>}
      <Button type="submit" variant="contained" loading={pending} loadingPosition="start" sx={{ alignSelf: 'flex-start' }}>
        Check
      </Button>
    </Stack>
  )
}
