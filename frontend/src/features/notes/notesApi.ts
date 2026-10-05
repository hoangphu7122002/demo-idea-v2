import { api } from '../../api/client'
import type { components } from '../../api/schema'
import { baseApi, fromApi, toApiError } from '../../services/baseApi'
import { summariseNote } from './summary'

export type Note = components['schemas']['NoteOut']
export type NoteIn = components['schemas']['NoteIn']

export const notesApi = baseApi.injectEndpoints({
  endpoints: (build) => ({
    getNotes: build.query<Note[], void>({
      queryFn: () => fromApi(() => api.GET('/api/notes')),
      providesTags: [{ type: 'Note', id: 'LIST' }],
    }),
    createNote: build.mutation<Note, NoteIn>({
      queryFn: (body) => fromApi(() => api.POST('/api/notes', { body })),
      invalidatesTags: [{ type: 'Note', id: 'LIST' }],
    }),
    // Queues a Celery job and polls it; the list refetches when the summary is stored.
    summariseNote: build.mutation<null, number>({
      queryFn: async (id) => {
        try {
          await summariseNote(id)
          return { data: null }
        } catch (e) {
          return { error: toApiError(e) }
        }
      },
      invalidatesTags: [{ type: 'Note', id: 'LIST' }],
    }),
  }),
})

export const { useGetNotesQuery, useCreateNoteMutation, useSummariseNoteMutation } = notesApi
