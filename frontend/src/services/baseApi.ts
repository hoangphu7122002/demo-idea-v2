import { createApi, fakeBaseQuery } from '@reduxjs/toolkit/query/react'

export interface ApiError {
  /** HTTP status, or 0 when the request never got a response. */
  status: number
  message: string
}

export function toApiError(e: unknown, status = 0): ApiError {
  return { status, message: e instanceof Error ? e.message : 'Something went wrong' }
}

type ApiResult<T> = { data?: T; error?: unknown; response: Response }

/**
 * Adapts an openapi-fetch call (`api.GET(...)`, `api.POST(...)`) to the `{ data } | { error }`
 * shape RTK Query's `queryFn` expects. Keeps the typed client as the only way to call the API.
 */
export async function fromApi<T>(call: () => Promise<ApiResult<T>>): Promise<{ data: T } | { error: ApiError }> {
  try {
    const { data, error, response } = await call()
    if (error !== undefined || !response.ok) {
      return { error: { status: response.status, message: `Request failed (${response.status})` } }
    }
    return { data: data as T }
  } catch (e) {
    return { error: toApiError(e) }
  }
}

/** Root API slice. Each feature adds endpoints with `baseApi.injectEndpoints` in `features/<feature>/<feature>Api.ts`. */
export const baseApi = createApi({
  reducerPath: 'api',
  baseQuery: fakeBaseQuery<ApiError>(),
  tagTypes: ['Note'],
  endpoints: () => ({}),
})
