import React, { useState, useRef, useEffect } from 'react'
import { getAIResponse } from '../services/api'
import type { Exercise } from '../types'

interface Message {
  who: 'user' | 'ai'
  text: string
  sql_query?: string
  query_result?: {
    columns: string[]
    rows: any[][]
    row_count: number
  }
  executed?: boolean
  intent?: string
}

interface Props {
  exercise: Exercise | null
  userQuery?: string
  error?: string
  demoMode: boolean
}

export default function AIChat({ exercise, userQuery, error, demoMode }: Props) {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
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
      setMessages((prev) => [
        ...prev,
        {
          who: 'ai',
          text: res.response,
          sql_query: res.sql_query,
          query_result: res.query_result,
          executed: res.executed,
          intent: res.intent,
        },
      ])
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

  const renderQueryResult = (result: Message['query_result']) => {
    if (!result || result.row_count === 0) return null

    return (
      <div className="mt-3 overflow-x-auto">
        <table className="min-w-full text-xs border border-gray-300 rounded">
          <thead className="bg-gray-50">
            <tr>
              {result.columns.map((col, i) => (
                <th key={i} className="px-3 py-2 text-left font-medium text-gray-700 border-b">
                  {col}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {result.rows.slice(0, 5).map((row, i) => (
              <tr key={i} className="border-b border-gray-200">
                {row.map((cell, j) => (
                  <td key={j} className="px-3 py-2 text-gray-900">
                    {cell === null ? (
                      <span className="text-gray-400 italic">null</span>
                    ) : (
                      String(cell)
                    )}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
        {result.row_count > 5 && (
          <p className="text-xs text-gray-500 mt-1">Showing 5 of {result.row_count} rows</p>
        )}
      </div>
    )
  }

  const renderMessage = (m: Message, i: number) => {
    if (m.who === 'user') {
      return (
        <div key={i} className="flex justify-end">
          <div className="max-w-[80%] px-4 py-3 rounded-xl bg-blue-600 text-white">
            <p className="text-sm whitespace-pre-wrap break-words">{m.text}</p>
          </div>
        </div>
      )
    }

    // AI message
    return (
      <div key={i} className="flex justify-start">
        <div className="max-w-[85%] bg-gray-100 text-gray-900 px-4 py-3 rounded-xl">
          {/* Main response text */}
          <p className="text-sm whitespace-pre-wrap break-words">{m.text}</p>

          {/* SQL Query display (if generated) */}
          {m.sql_query && (
            <div className="mt-3 bg-gray-800 text-gray-100 p-3 rounded-lg overflow-x-auto">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-mono text-gray-400">Generated SQL</span>
                {m.executed && (
                  <span className="text-xs bg-green-600 text-white px-2 py-0.5 rounded">
                    ✓ Executed
                  </span>
                )}
              </div>
              <pre className="text-xs font-mono">{m.sql_query}</pre>
            </div>
          )}

          {/* Query result table (if executed) */}
          {m.executed && m.query_result && renderQueryResult(m.query_result)}
        </div>
      </div>
    )
  }

  return (
    <div className="h-full flex flex-col bg-white rounded-xl border border-gray-200 overflow-hidden">
      {/* Header */}
      <div className="h-14 shrink-0 px-6 border-b border-gray-200 flex items-center">
        <h3 className="text-sm font-medium text-gray-900">AI assistant</h3>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-auto p-6 space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-center text-gray-400 text-sm">
            <div>
              <p>No messages yet.</p>
              <p className="mt-1">Ask the AI for help with your SQL query!</p>
              <div className="mt-4 text-xs space-y-1">
                <p className="text-gray-500">Try asking:</p>
                <p className="text-blue-500">"How many problems did I solve?"</p>
                <p className="text-blue-500">"Show me my progress"</p>
                <p className="text-blue-500">"What is a JOIN?"</p>
              </div>
            </div>
          </div>
        ) : (
          messages.map(renderMessage)
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
