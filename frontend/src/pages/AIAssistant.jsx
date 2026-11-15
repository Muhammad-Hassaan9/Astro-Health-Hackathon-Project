import { Bot, ShieldCheck, Sparkles } from 'lucide-react'
import ChatWindow from '../features/ai-assistant/components/ChatWindow'
import useAIChat from '../features/ai-assistant/hooks/useAIChat'

const suggestions = [
  'What does my heart rate indicate?',
  'How can I improve my sleep quality?',
  'Why is oxygen saturation important?',
]

export default function AIAssistant() {
  const { messages, loading, sendMessage } = useAIChat()

  return (
    <div className="space-y-6">
      <div>
        <div className="mb-2 flex items-center gap-2 text-cyan-400">
          <Sparkles size={18} />
          <span className="text-sm font-medium">AI-Powered Guidance</span>
        </div>

        <h1 className="text-2xl font-bold text-white sm:text-3xl">
          AI Assistant
        </h1>

        <p className="mt-2 text-sm text-slate-400">
          Ask questions and get general health and wellness guidance for your
          space mission.
        </p>
      </div>

      <div className="grid gap-3 sm:grid-cols-2">
        <div className="flex items-start gap-3 rounded-xl border border-slate-700 bg-slate-900 p-4">
          <Bot className="mt-1 shrink-0 text-cyan-400" size={20} />
          <div>
            <h3 className="text-sm font-semibold text-white">
              AI Health Guidance
            </h3>
            <p className="mt-1 text-xs leading-5 text-slate-400">
              Get explanations and general wellness suggestions.
            </p>
          </div>
        </div>

        <div className="flex items-start gap-3 rounded-xl border border-slate-700 bg-slate-900 p-4">
          <ShieldCheck
            className="mt-1 shrink-0 text-emerald-400"
            size={20}
          />
          <div>
            <h3 className="text-sm font-semibold text-white">
              Safety First
            </h3>
            <p className="mt-1 text-xs leading-5 text-slate-400">
              AI guidance is informational and does not replace professional
              medical advice.
            </p>
          </div>
        </div>
      </div>

      <ChatWindow
        messages={messages}
        loading={loading}
        onSend={sendMessage}
      />

      <div>
        <p className="mb-3 text-xs font-medium uppercase tracking-wider text-slate-500">
          Suggested questions
        </p>

        <div className="flex flex-wrap gap-2">
          {suggestions.map((suggestion) => (
            <button
              key={suggestion}
              type="button"
              onClick={() => sendMessage(suggestion)}
              disabled={loading}
              className="rounded-full border border-slate-700 bg-slate-900 px-3 py-2 text-left text-xs text-slate-300 transition hover:border-cyan-500 hover:text-cyan-400 disabled:opacity-40"
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}