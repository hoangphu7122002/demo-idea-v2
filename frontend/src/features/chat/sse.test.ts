import { expect, test } from 'vitest'
import { readSse } from './sse'

test('parses SSE frames split across chunks', async () => {
  const chunks = ['data: {"type":"tool","name":"t"}\n\nda', 'ta: {"type":"delta","text":"hi"}\n\n', 'data: {"type":"done"}\n\n']
  const body = new ReadableStream<Uint8Array>({
    start(c) {
      chunks.forEach((s) => c.enqueue(new TextEncoder().encode(s)))
      c.close()
    },
  })
  const events = []
  for await (const ev of readSse(body)) events.push(ev)
  expect(events).toEqual([{ type: 'tool', name: 't' }, { type: 'delta', text: 'hi' }, { type: 'done' }])
})
