import { Bot, User, AlertCircle } from 'lucide-react'

export default function ChatMessage({ message }) {
  const isAssistant = message.role === 'assistant'

  return (
    <div
      className={`flex gap-3 ${
        isAssistant ? 'justify-start' : 'justify-end'
      }`}
    >
      {isAssistant && (
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-cyan-500/10 text-cyan-400">
          <Bot size={19} />
        </div>
      )}

      <div
        className={`max-w-[85%] rounded-2xl px-4 py-3 sm:max-w-[75%] ${
          isAssistant
            ? 'rounded-tl-sm border border-slate-700 bg-slate-800/80 text-slate-200'
            : 'rounded-tr-sm bg-cyan-600 text-white'
        }`}
      >
        {message.isError && (
          <div className="mb-2 flex items-center gap-2 text-sm text-red-400">
            <AlertCircle size={15} />
            <span>Response error</span>
          </div>
        )}

        <p className="whitespace-pre-wrap text-sm leading-6">
          {message.content}
        </p>
      </div>

      {!isAssistant && (
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-slate-700 text-slate-300">
          <User size={19} />
        </div>
      )}
    </div>
  )
}