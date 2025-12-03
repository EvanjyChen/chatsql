import React from 'react'
import Editor from '@monaco-editor/react'
import type { Exercise, QueryResult, SubmitResult } from '../types'
import { executeQuery, submitQuery } from '../services/api'

interface Props {
  value: string
  onChange: (v: string) => void
  exercise: Exercise | null
  onExecute: (r: QueryResult) => void
  onSubmit: (r: SubmitResult) => void
  isLoading: boolean
  demoMode: boolean
}

export default function CodeEditor({
  value,
  onChange,
  exercise,
  onExecute,
  onSubmit,
  isLoading,
  demoMode,
}: Props) {
  const handleRun = async () => {
    if (!exercise) return
    try {
      const res = await executeQuery(exercise.id, value, demoMode)
      onExecute(res)
    } catch (e) {
      console.error(e)
    }
  }

  const handleSubmit = async () => {
    if (!exercise) return
    try {
      const res = await submitQuery(exercise.id, value, demoMode)
      onSubmit(res)
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <div className="h-full flex flex-col bg-white rounded-xl border border-gray-200 overflow-hidden">
      {/* Header with title and buttons */}
      <div className="h-14 shrink-0 flex items-center justify-between px-6 border-b border-gray-200">
        <div className="flex items-center gap-3 min-w-0 flex-1">
          <h3 className="text-sm text-gray-900 truncate">
            {exercise ? exercise.title : 'Code Editor'}
          </h3>
          {exercise && (
            <span className="text-xs px-2 py-1 rounded-md bg-gray-100 text-gray-600 shrink-0">
              {exercise.difficulty}
            </span>
          )}
        </div>

        <div className="flex items-center gap-2 shrink-0">
          <button
            onClick={handleRun}
            disabled={isLoading || !exercise}
            className="px-4 py-1.5 text-sm font-medium text-green-600 hover:bg-green-50 rounded-full disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
          >
            Run
          </button>
          <button
            onClick={handleSubmit}
            disabled={isLoading || !exercise}
            className="px-4 py-1.5 text-sm font-medium text-blue-600 hover:bg-blue-50 rounded-full disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
          >
            Submit
          </button>
        </div>
      </div>

      {/* Editor */}
      <div className="flex-1 min-h-0">
        <Editor
          height="100%"
          defaultLanguage="sql"
          value={value}
          onChange={(v) => onChange(v || '')}
          theme="vs-light"
          options={{
            minimap: { enabled: false },
            fontSize: 14,
            lineNumbers: 'on',
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 2,
          }}
        />
      </div>
    </div>
  )
}
