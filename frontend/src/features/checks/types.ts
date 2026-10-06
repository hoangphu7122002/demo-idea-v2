/** Field names match the planned check API; swap for the generated schema types in check-wire. */
export interface Flag {
  paragraph_id: string
  reason: string
  source_quote: string
  proposed_fix: string
}

export type CheckSource = 'live' | 'cache'

export interface CheckInput {
  release_url?: string
  release_text?: string
}
