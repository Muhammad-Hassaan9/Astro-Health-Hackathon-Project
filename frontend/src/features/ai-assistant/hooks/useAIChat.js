import { useState } from 'react'
import { api } from '../../../lib/api'

export default function useAIChat() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content:
        "Hello! I'm AstroHealth AI Assistant. I can help you understand your health readings and provide general wellness guidance. What would you like to know?",
    },
  ])

  const [loading, setLoading] = useState(false)

  const sendMessage = async (question) => {
    const trimmedQuestion = question.trim()

    if (!trimmedQuestion || loading) return

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: trimmedQuestion,
    }

    setMessages((previous) => [...previous, userMessage])
    setLoading(true)

    try {
      const response = await api.post('/ai/guidance', {
        question: trimmedQuestion,
      })

      setMessages((previous) => [
        ...previous,
        {
          id: Date.now() + 1,
          role: 'assistant',
          content: response.data.answer || 'I could not generate a response.',
        },
      ])
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.response?.data?.message ||
        'Unable to connect to the AI assistant. Please try again.'

      setMessages((previous) => [
        ...previous,
        {
          id: Date.now() + 1,
          role: 'assistant',
          content: errorMessage,
          isError: true,
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  return {
    messages,
    loading,
    sendMessage,
  }
}