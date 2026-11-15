import { useState } from 'react'
import { Send } from 'lucide-react'

export default function ChatInput({ onSend, loading }) {
  const [message, setMessage] = useState('')

  const handleSubmit = (event) => {
    event.preventDefault()

    if (!message.trim() || loading) return

    onSend(message)
    setMessage('')
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="flex items-end gap-3 border-t border-slate-700 bg-slate-900/80 p-3 sm:p-4"
    >
      <textarea
        value={message}
        onChange={(event) => setMessage(event.target.value)}
        onKeyDown={(event) => {
          if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault()
            handleSubmit(event)
          }
        }}
        placeholder="Ask something about your health..."
        rows={1}
        disabled={loading}
        className="max-h-32 min-h-12 flex-1 resize-y rounded-xl border border-slate-700 bg-slate-800 px-4 py-3 text-sm text-white outline-none placeholder:text-slate-500 focus:border-cyan-500 disabled:opacity-50"
      />

      <button
        type="submit"
        disabled={!message.trim() || loading}
        className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-cyan-600 text-white transition hover:bg-cyan-500 disabled:cursor-not-allowed disabled:opacity-40"
        aria-label="Send message"
      >
        <Send size={18} />
      </button>
    </form>
  )
}