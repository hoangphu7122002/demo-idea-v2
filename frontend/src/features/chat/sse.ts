export type ChatEvent = { type: 'delta'; text: string } | { type: 'tool'; name: string } | { type: 'done' }

/** Read a text/event-stream body and yield parsed `data:` JSON events. */
export async function* readSse(body: ReadableStream<Uint8Array>): AsyncGenerator<ChatEvent> {
  const reader = body.getReader()
  const decoder = new TextDecoder()
  let buf = ''
  for (;;) {
    const { value, done } = await reader.read()
    if (done) return
    buf += decoder.decode(value, { stream: true })
    let i: number
    while ((i = buf.indexOf('\n\n')) >= 0) {
      const frame = buf.slice(0, i)
      buf = buf.slice(i + 2)
      if (frame.startsWith('data: ')) yield JSON.parse(frame.slice(6)) as ChatEvent
    }
  }
}
