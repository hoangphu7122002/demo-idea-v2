import { PageHeader } from '../components/PageHeader'
import { ChatPanel } from '../features/chat/ChatPanel'

export function ChatPage() {
  return (
    <>
      <PageHeader title="Chat" />
      <ChatPanel />
    </>
  )
}
