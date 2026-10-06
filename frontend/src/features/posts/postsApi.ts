import { api } from '../../api/client'
import type { components } from '../../api/schema'
import { baseApi, fromApi } from '../../services/baseApi'

export type Post = components['schemas']['PostOut']

export const postsApi = baseApi.injectEndpoints({
  endpoints: (build) => ({
    getPost: build.query<Post, string>({
      queryFn: (slug) => fromApi(() => api.GET('/api/posts/{slug}', { params: { path: { slug } } })),
    }),
  }),
})

export const { useGetPostQuery } = postsApi
