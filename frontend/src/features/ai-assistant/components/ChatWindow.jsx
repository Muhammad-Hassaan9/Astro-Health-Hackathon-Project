import { useEffect, useRef } from 'react'
import { Bot, LoaderCircle } from 'lucide-react'
import ChatMessage from './ChatMessage'
import ChatInput from './ChatInput'

export default function ChatWindow({ messages, loading, onSend }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  return (
    <div className="flex h-[min(680px,calc(100vh-220px))] min-h-[420px] flex-col overflow-hidden rounded-2xl border border-slate-700 bg-slate-900 shadow-xl">
      <div className="flex items-center gap-3 border-b border-slate-700 px-4 py-4">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-cyan-500/10 text-cyan-400">
          <Bot size={22} />
        </div>

        <div>
          <h2 className="font-semibold text-white">AstroHealth AI</h2>
          <p className="text-xs text-emerald-400">AI Assistant</p>
        </div>
      </div>

      <div className="flex-1 space-y-5 overflow-y-auto p-4 sm:p-5">
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}

        {loading && (
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-cyan-500/10 text-cyan-400">
              <Bot size={19} />
            </div>

            <div className="flex items-center gap-2 rounded-2xl rounded-tl-sm border border-slate-700 bg-slate-800 px-4 py-3 text-sm text-slate-400">
              <LoaderCircle size={16} className="animate-spin" />
              Generating response...
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      <ChatInput onSend={onSend} loading={loading} />
    </div>
  )
}