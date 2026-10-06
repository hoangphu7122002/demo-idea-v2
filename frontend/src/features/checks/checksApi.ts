import { api } from '../../api/client'
import type { components } from '../../api/schema'
import { baseApi, fromApi, toApiError, type ApiError } from '../../services/baseApi'

export type CheckResult = components['schemas']['CheckOut']
export type Flag = components['schemas']['FlagOut']
export type CheckInput = components['schemas']['CheckIn']
/** `null`/absent when the flags come from GET (the source of the original run is not stored). */
export type CheckSource = NonNullable<CheckResult['source']>

/** FastAPI errors carry `detail`: a message string, or a list of validation errors. */
function detailMessage(error: unknown): string | undefined {
  const detail = error && typeof error === 'object' && 'detail' in error ? error.detail : undefined
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail) && detail.length > 0 && typeof detail[0]?.msg === 'string') return detail[0].msg
  return undefined
}

export function checkErrorMessage(status: number, error: unknown): string {
  if (status === 503) return 'Check unavailable, try again'
  if (status === 404) return 'Post not found'
  return detailMessage(error) ?? `Request failed (${status})`
}

export const checksApi = baseApi.injectEndpoints({
  endpoints: (build) => ({
    getFlags: build.query<CheckResult | null, string>({
      queryFn: (slug) => fromApi(() => api.GET('/api/posts/{slug}/flags', { params: { path: { slug } } })),
      providesTags: (_r, _e, slug) => [{ type: 'Check', id: slug }],
    }),
    checkPost: build.mutation<CheckResult, { slug: string; body: CheckInput }>({
      queryFn: async ({ slug, body }) => {
        try {
          const { data, error, response } = await api.POST('/api/posts/{slug}/check', { params: { path: { slug } }, body })
          if (data !== undefined && response.ok) return { data }
          const apiError: ApiError = { status: response.status, message: checkErrorMessage(response.status, error) }
          return { error: apiError }
        } catch (e) {
          return { error: toApiError(e) }
        }
      },
      invalidatesTags: (_r, _e, { slug }) => [{ type: 'Check', id: slug }],
    }),
  }),
})

export const { useGetFlagsQuery, useCheckPostMutation } = checksApi
