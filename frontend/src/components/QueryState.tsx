import Alert from '@mui/material/Alert'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import CircularProgress from '@mui/material/CircularProgress'
import Typography from '@mui/material/Typography'
import type { ReactNode } from 'react'

interface QueryLike<T> {
  data?: T
  isLoading: boolean
  isError: boolean
  error?: unknown
  refetch: () => unknown
}

interface QueryStateProps<T> {
  query: QueryLike<T>
  /** Treat the loaded data as empty (defaults to empty arrays). */
  isEmpty?: (data: T) => boolean
  emptyMessage?: ReactNode
  children: (data: T) => ReactNode
}

function errorMessage(error: unknown): string {
  if (error && typeof error === 'object' && 'message' in error) return String(error.message)
  return 'Something went wrong.'
}

const defaultIsEmpty = (data: unknown) => Array.isArray(data) && data.length === 0

/** Loading, error (with retry), empty, or loaded state for an RTK Query result. Use it for every list or detail view. */
export function QueryState<T>({ query, isEmpty = defaultIsEmpty, emptyMessage = 'Nothing here yet.', children }: QueryStateProps<T>) {
  if (query.isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 6 }} role="status" aria-label="Loading">
        <CircularProgress size={28} />
      </Box>
    )
  }
  if (query.isError || query.data === undefined) {
    return (
      <Alert
        severity="error"
        action={
          <Button color="inherit" size="small" onClick={() => query.refetch()}>
            Retry
          </Button>
        }
      >
        {errorMessage(query.error)}
      </Alert>
    )
  }
  if (isEmpty(query.data)) {
    return (
      <Typography color="text.secondary" sx={{ textAlign: 'center', py: 6 }}>
        {emptyMessage}
      </Typography>
    )
  }
  return <>{children(query.data)}</>
}
