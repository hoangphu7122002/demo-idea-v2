import { z } from 'zod'

export const noteFormSchema = z.object({
  title: z.string().trim().min(1, 'Title is required').max(200),
  body: z.string().trim().min(1, 'Body is required'),
})

export type NoteFormValues = z.infer<typeof noteFormSchema>
