import { z } from 'zod'

export const checkFormSchema = z
  .object({
    release_url: z.string().trim().refine((v) => v === '' || /^https?:\/\/\S+$/i.test(v), 'Enter a valid http(s) URL'),
    release_text: z.string().trim(),
  })
  .refine((v) => v.release_url !== '' || v.release_text !== '', {
    path: ['release_url'],
    message: 'Enter a release URL or paste release text',
  })

export type CheckFormValues = z.infer<typeof checkFormSchema>
