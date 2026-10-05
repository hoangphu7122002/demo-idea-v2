import Button from '@mui/material/Button'
import Dialog from '@mui/material/Dialog'
import DialogActions from '@mui/material/DialogActions'
import DialogContent from '@mui/material/DialogContent'
import DialogTitle from '@mui/material/DialogTitle'
import Stack from '@mui/material/Stack'
import { useId, type FormEventHandler, type ReactNode } from 'react'

interface FormDialogProps {
  open: boolean
  title: ReactNode
  onClose: () => void
  onSubmit: FormEventHandler<HTMLFormElement>
  submitLabel?: string
  submitting?: boolean
  children: ReactNode
}

/** Dialog shell for a form: title, stacked fields, cancel/submit actions. */
export function FormDialog({ open, title, onClose, onSubmit, submitLabel = 'Save', submitting = false, children }: FormDialogProps) {
  const titleId = useId()
  return (
    <Dialog open={open} onClose={submitting ? undefined : onClose} aria-labelledby={titleId}>
      <form onSubmit={onSubmit} noValidate>
        <DialogTitle id={titleId}>{title}</DialogTitle>
        <DialogContent>
          <Stack spacing={2} sx={{ pt: 1 }}>
            {children}
          </Stack>
        </DialogContent>
        <DialogActions sx={{ px: 3, pb: 2 }}>
          <Button onClick={onClose} disabled={submitting}>
            Cancel
          </Button>
          <Button type="submit" variant="contained" loading={submitting}>
            {submitLabel}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  )
}
