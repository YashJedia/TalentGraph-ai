import { useState } from 'react'
import { api } from '../services/api'

type ChatMessage = {
  role: 'user' | 'assistant'
  text: string
}

export default function RecruiterCopilot() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSend = async () => {
    if (!input.trim()) {
      return
    }

    const userMessage: ChatMessage = {
      role: 'user',
      text: input.trim(),
    }
    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await api.askCopilot(userMessage.text)
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        text: response.data.message,
      }
      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      console.error('Copilot request failed', error)
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', text: 'Unable to reach the assistant. Please try again later.' },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-semibold text-white">Recruiter Copilot</h1>
        <p className="mt-3 text-slate-400 max-w-2xl">Ask the AI assistant about candidates, rankings, and hiring recommendations.</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[1fr_360px]">
        <div className="rounded-[32px] border border-white/10 bg-slate-900/95 p-7 shadow-[0_28px_80px_rgba(15,23,42,0.35)]">
          <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <h2 className="text-xl font-semibold text-white">Chat with Copilot</h2>
              <p className="mt-2 text-sm text-slate-400">Ask questions about candidate fit, ranking differences, or hiring strategy.</p>
            </div>
            <span className="inline-flex rounded-2xl bg-slate-800 px-4 py-2 text-sm text-slate-200 shadow-inner shadow-slate-950/20">AI</span>
          </div>

          <div className="space-y-4">
            {messages.length === 0 ? (
              <div className="rounded-3xl border border-dashed border-slate-700 bg-slate-950/95 p-8 text-center text-slate-500">
                Start the conversation by asking a recruiting question.
              </div>
            ) : (
              <div className="space-y-4 max-h-[54vh] overflow-y-auto pr-2">
                {messages.map((message, index) => (
                  <div
                    key={`${message.role}-${index}`}
                    className={`rounded-3xl p-4 ${message.role === 'user' ? 'bg-slate-900 text-slate-100' : 'bg-slate-800/90 text-slate-200'}`}
                  >
                    <p className="text-xs uppercase tracking-[0.24em] text-slate-500">{message.role === 'user' ? 'You' : 'Assistant'}</p>
                    <p className="mt-3 whitespace-pre-line leading-7">{message.text}</p>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="mt-6 rounded-3xl border border-slate-800 bg-slate-950/95 p-5">
            <textarea
              value={input}
              onChange={(event) => setInput(event.target.value)}
              rows={5}
              className="w-full resize-none rounded-3xl border border-slate-700 bg-slate-950 px-4 py-4 text-slate-100 outline-none focus:border-sky-500"
              placeholder="Ask the recruiter copilot about candidate fit, hidden gems, or fraud risk..."
            />
            <button
              type="button"
              onClick={handleSend}
              disabled={loading}
              className="mt-4 rounded-3xl bg-gradient-to-r from-sky-500 to-violet-600 px-5 py-4 text-sm font-semibold text-white shadow-lg shadow-sky-500/20 transition hover:from-sky-400 hover:to-violet-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? 'Sending…' : 'Send'}
            </button>
          </div>
        </div>

        <div className="rounded-[32px] border border-white/10 bg-slate-900/95 p-7 shadow-[0_28px_80px_rgba(15,23,42,0.35)]">
          <h2 className="text-xl font-semibold text-white">Suggested questions</h2>
          <div className="mt-5 space-y-3">
            {[
              'Why is Candidate A ranked higher than Candidate B?',
              'Identify top hidden gem candidates for this job.',
              'What fraud signals should I review first?',
            ].map((question) => (
              <button
                key={question}
                type="button"
                onClick={() => setInput(question)}
                className="w-full rounded-3xl border border-slate-800 bg-slate-950 px-4 py-4 text-left text-sm text-slate-200 transition hover:border-sky-500 hover:bg-slate-900/95"
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
