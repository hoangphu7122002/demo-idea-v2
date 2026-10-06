import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import { useParams } from 'react-router'
import { PageHeader } from '../components/PageHeader'
import { QueryState } from '../components/QueryState'
import { CheckPanel } from '../features/checks/CheckPanel'
import { CheckResults } from '../features/checks/CheckResults'
import { useCheckPostMutation, useGetFlagsQuery, type CheckInput } from '../features/checks/checksApi'
import PostBody from '../features/posts/PostBody'
import { useGetPostQuery } from '../features/posts/postsApi'
import { NotFoundPage } from './NotFoundPage'

function statusOf(error: unknown): number | undefined {
  return error && typeof error === 'object' && 'status' in error && typeof error.status === 'number' ? error.status : undefined
}

/** Route component. `key={slug}` remounts the view per post, so check state never leaks from one post to another. */
export function PostPage() {
  const { slug = '' } = useParams()
  return <PostView key={slug} slug={slug} />
}

function PostView({ slug }: { slug: string }) {
  const query = useGetPostQuery(slug)
  const flagsQuery = useGetFlagsQuery(slug)
  const [checkPost, check] = useCheckPostMutation()
  if (statusOf(query.error) === 404) return <NotFoundPage />

  // The fresh check result knows its source (live/cache); the GET only has the latest flags.
  const latest = check.data ?? flagsQuery.data ?? null
  const error = check.error && typeof check.error === 'object' && 'message' in check.error ? String(check.error.message) : undefined
  const onCheck = (body: CheckInput) => checkPost({ slug, body }).unwrap().catch(() => undefined)
  const onSelect = (id: string) => document.getElementById(id)?.scrollIntoView?.({ behavior: 'smooth', block: 'start' })

  return (
    <QueryState query={query}>
      {(post) => (
        <>
          <Box sx={{ maxWidth: 720, mx: 'auto' }}>
            <PageHeader title={post.title} />
            <Stack spacing={3} sx={{ mb: 4 }}>
              <CheckPanel onCheck={onCheck} pending={check.isLoading} error={error} />
              {latest && <CheckResults flags={latest.flags} source={latest.source} onSelect={onSelect} />}
            </Stack>
          </Box>
          <PostBody paragraphs={post.paragraphs} flaggedIds={latest?.flags.map((f) => f.paragraph_id)} />
        </>
      )}
    </QueryState>
  )
}
