import { useSnackbar } from 'notistack'
import { useCallback } from 'react'

interface Messages {
  success: string
  error: string
}

/**
 * Run a mutation and toast the outcome. Returns true on success so the caller can close a dialog or reset a form.
 *   const run = useMutationToast()
 *   if (await run(createNote(values).unwrap(), { success: 'Note added', error: 'Could not add note' })) reset()
 */
export function useMutationToast() {
  const { enqueueSnackbar } = useSnackbar()
  return useCallback(
    async (promise: Promise<unknown>, messages: Messages) => {
      try {
        await promise
        enqueueSnackbar(messages.success, { variant: 'success' })
        return true
      } catch (e) {
        const detail = e && typeof e === 'object' && 'message' in e ? `: ${String(e.message)}` : ''
        enqueueSnackbar(messages.error + detail, { variant: 'error' })
        return false
      }
    },
    [enqueueSnackbar],
  )
}
