import React, { useState, useRef, useEffect } from 'react'
import { getAIResponse } from '../services/api'
import type { Exercise } from '../types'

interface Props {
  exercise: Exercise | null
  userQuery?: string
  error?: string
  demoMode: boolean
}

export default function AIChat({ exercise, userQuery, error, demoMode }: Props) {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState<{ who: 'user' | 'ai'; text: string }[]>([])
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const send = async () => {
    if (!exercise || !input.trim()) return

    setMessages((prev) => [...prev, { who: 'user', text: input }])
    const msg = input
    setInput('')
    setLoading(true)

    try {
      const res = await getAIResponse(exercise.id, msg, userQuery, error, demoMode)
      setMessages((prev) => [...prev, { who: 'ai', text: res.response }])
    } catch (e) {
      setMessages((prev) => [...prev, { who: 'ai', text: 'Error contacting AI' }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      send()
    }
  }

  return (
    <div className="h-full flex flex-col bg-white rounded-xl border border-gray-200 overflow-hidden">
      {/* Header */}
      <div className="h-14 shrink-0 px-6 border-b border-gray-200 flex items-center">
        <h3 className="text-sm text-gray-900">AI assistant</h3>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-auto p-6 space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-center text-gray-400 text-sm">
            <div>
              <p>No messages yet.</p>
              <p className="mt-1">Ask the AI for help with your SQL query!</p>
            </div>
          </div>
        ) : (
          messages.map((m, i) => (
            <div key={i} className={`flex ${m.who === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div
                className={`max-w-[80%] px-4 py-3 rounded-xl ${
                  m.who === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-900'
                }`}
              >
                <p className="text-sm whitespace-pre-wrap break-words">{m.text}</p>
              </div>
            </div>
          ))
        )}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 text-gray-900 px-4 py-3 rounded-xl">
              <p className="text-sm">Thinking...</p>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-gray-200 p-4 bg-white">
        <div className="relative">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            className="w-full pl-4 pr-12 py-3 rounded-full border border-gray-300 bg-white text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-sm"
            placeholder="Ask anything"
            disabled={loading || !exercise}
          />
          <button
            onClick={send}
            disabled={loading || !exercise || !input.trim()}
            className="absolute right-2 top-1/2 -translate-y-1/2 w-8 h-8 flex items-center justify-center bg-blue-600 text-white rounded-full hover:bg-blue-700 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
            aria-label="Send message"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 10l7-7m0 0l7 7m-7-7v18"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  )
}