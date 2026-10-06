import { z } from 'zod'

export const checkFormSchema = z
  .object({
    resource_url: z.string().trim().refine((v) => v === '' || /^https?:\/\/\S+$/i.test(v), 'Enter a valid http(s) URL'),
    resource_text: z.string().trim(),
  })
  .refine((v) => v.resource_url !== '' || v.resource_text !== '', {
    path: ['resource_url'],
    message: 'Enter a resource URL or paste resource text',
  })

export type CheckFormValues = z.infer<typeof checkFormSchema>
