// ProblemDescription.tsx - 完整版本
import React, { useState } from 'react'
import type { Exercise } from '../types'

interface Props {
  exercise: Exercise | null
}

type Tab = 'description' | 'solution' | 'submissions' | 'notes'

export default function ProblemDescription({ exercise }: Props) {
  const [activeTab, setActiveTab] = useState<Tab>('description')

  if (!exercise)
    return (
      <div className="h-full flex items-center justify-center text-sm text-gray-500">
        Select an exercise to begin
      </div>
    )

  return (
    <div className="h-full flex flex-col bg-white rounded-xl border border-gray-200">
      {/* Tabs */}
      <div className="h-14 shrink-0 border-b border-gray-200 px-6 flex items-center overflow-x-auto">
        <div className="flex gap-7">
          <button
            onClick={() => setActiveTab('description')}
            className={`text-sm font-medium transition-colors whitespace-nowrap ${
              activeTab === 'description' ? 'text-blue-600' : 'text-gray-500 hover:text-gray-900'
            }`}
          >
            Description
          </button>
          <button
            onClick={() => setActiveTab('solution')}
            className={`text-sm font-medium transition-colors whitespace-nowrap ${
              activeTab === 'solution' ? 'text-blue-600' : 'text-gray-500 hover:text-gray-900'
            }`}
          >
            Solution
          </button>
          <button
            onClick={() => setActiveTab('submissions')}
            className={`text-sm font-medium transition-colors whitespace-nowrap ${
              activeTab === 'submissions' ? 'text-blue-600' : 'text-gray-500 hover:text-gray-900'
            }`}
          >
            Submissions
          </button>
          <button
            onClick={() => setActiveTab('notes')}
            className={`text-sm font-medium transition-colors whitespace-nowrap ${
              activeTab === 'notes' ? 'text-blue-600' : 'text-gray-500 hover:text-gray-900'
            }`}
          >
            Notes
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-auto p-6">
        {activeTab === 'description' && (
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-3">{exercise.title}</h2>
            <div className="flex items-center gap-3 text-sm text-gray-600 mb-6">
              <span>{exercise.schema.display_name}</span>
              <span>•</span>
              <span className="px-2 py-1 rounded-md bg-gray-100 text-gray-700">
                {exercise.difficulty}
              </span>
            </div>
            <div className="text-sm text-gray-700 whitespace-pre-wrap leading-relaxed">
              {exercise.description}
            </div>
          </div>
        )}

        {activeTab === 'solution' && (
          <div>
            <h3 className="text-base font-semibold text-gray-900 mb-4">Solution</h3>
            <p className="text-sm text-gray-600">Solution will be available after submission.</p>
          </div>
        )}

        {activeTab === 'submissions' && (
          <div>
            <h3 className="text-base font-semibold text-gray-900 mb-4">Submissions</h3>
            <p className="text-sm text-gray-600">Your submission history will appear here.</p>
          </div>
        )}

        {activeTab === 'notes' && (
          <div>
            <h3 className="text-base font-semibold text-gray-900 mb-4">Notes</h3>
            <ul className="space-y-2 list-disc list-inside text-sm text-gray-600">
              <li>Focus on query correctness and efficiency</li>
              <li>Consider edge cases in your SQL</li>
              <li>Test with different data scenarios</li>
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}
