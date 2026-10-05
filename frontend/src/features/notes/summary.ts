import { api } from '../../api/client'

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms))

/** Queue a summary job and poll it until it finishes. Throws with a readable message on failure. */
export async function summariseNote(noteId: number, pollMs = 500, maxPolls = 60): Promise<void> {
  const { data, error } = await api.POST('/api/notes/{note_id}/summary', {
    params: { path: { note_id: noteId } },
  })
  if (error || !data) throw new Error('Could not start summary')
  for (let i = 0; i < maxPolls; i++) {
    const { data: job } = await api.GET('/api/jobs/{job_id}', { params: { path: { job_id: data.job_id } } })
    if (job?.status === 'done') return
    if (job?.status === 'failed') throw new Error(job.error ?? 'Summary failed')
    await sleep(pollMs)
  }
  throw new Error('Summary timed out')
}
