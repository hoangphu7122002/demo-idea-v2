import Box from '@mui/material/Box'
import { useParams } from 'react-router'
import { PageHeader } from '../components/PageHeader'
import { QueryState } from '../components/QueryState'
import PostBody from '../features/posts/PostBody'
import { useGetPostQuery } from '../features/posts/postsApi'
import { NotFoundPage } from './NotFoundPage'

export function PostPage() {
  const { slug = '' } = useParams()
  const query = useGetPostQuery(slug)
  const status = query.error && typeof query.error === 'object' && 'status' in query.error ? query.error.status : undefined
  if (status === 404) return <NotFoundPage />

  return (
    <QueryState query={query}>
      {(post) => (
        <>
          <Box sx={{ maxWidth: 720, mx: 'auto' }}>
            <PageHeader title={post.title} />
          </Box>
          <PostBody paragraphs={post.paragraphs} />
        </>
      )}
    </QueryState>
  )
}
