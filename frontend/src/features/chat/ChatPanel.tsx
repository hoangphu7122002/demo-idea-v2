import SendIcon from '@mui/icons-material/Send'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Chip from '@mui/material/Chip'
import Paper from '@mui/material/Paper'
import Stack from '@mui/material/Stack'
import TextField from '@mui/material/TextField'
import Typography from '@mui/material/Typography'
import { useState, type FormEvent } from 'react'
import { readSse } from './sse'

type Msg = { role: 'user' | 'assistant'; text: string; tools: string[] }

export function ChatPanel() {
  const [msgs, setMsgs] = useState<Msg[]>([])
  const [input, setInput] = useState('')
  const [busy, setBusy] = useState(false)

  async function send(e: FormEvent) {
    e.preventDefault()
    const message = input
    setInput('')
    setBusy(true)
    setMsgs((m) => [...m, { role: 'user', text: message, tools: [] }, { role: 'assistant', text: '', tools: [] }])
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message }),
    })
    if (!res.ok || !res.body) {
      setBusy(false)
      return
    }
    for await (const ev of readSse(res.body)) {
      setMsgs((m) => {
        const last = { ...m[m.length - 1] }
        if (ev.type === 'delta') last.text += ev.text
        if (ev.type === 'tool') last.tools = [...last.tools, ev.name]
        return [...m.slice(0, -1), last]
      })
    }
    setBusy(false)
  }

  return (
    <Paper component="section" sx={{ p: 2 }}>
      <Stack spacing={1.5}>
        {msgs.map((m, i) => (
          <Box key={i} sx={{ alignSelf: m.role === 'user' ? 'flex-end' : 'flex-start', maxWidth: '85%' }}>
            <Typography variant="caption" color="text.secondary">
              {m.role}
            </Typography>
            {m.tools.map((t, j) => (
              <Chip key={j} label={`tool ${t}`} variant="outlined" sx={{ ml: 1 }} />
            ))}
            <Typography
              sx={{
                px: 1.5,
                py: 1,
                borderRadius: 2,
                bgcolor: m.role === 'user' ? 'primary.main' : 'action.hover',
                color: m.role === 'user' ? 'primary.contrastText' : 'text.primary',
                whiteSpace: 'pre-wrap',
              }}
            >
              {m.text || '…'}
            </Typography>
          </Box>
        ))}
        <Stack component="form" direction="row" spacing={1} onSubmit={send}>
          <TextField label="Message" value={input} onChange={(e) => setInput(e.target.value)} />
          <Button type="submit" variant="contained" endIcon={<SendIcon />} disabled={busy || !input}>
            Send
          </Button>
        </Stack>
      </Stack>
    </Paper>
  )
}
