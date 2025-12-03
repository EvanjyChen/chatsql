import React, { useState } from 'react'
import type { Exercise } from '../types'

interface Props {
  exercise: Exercise | null
}

type Tab = 'description' | 'solution' | 'submissions'

export default function ProblemDescription({ exercise }: Props) {
  const [activeTab, setActiveTab] = useState<Tab>('description')

  if (!exercise) return <div className="h-full bg-white" />

  const tabs: { id: Tab; label: string }[] = [
    { id: 'description', label: 'Description' },
    { id: 'solution', label: 'Solution' },
    { id: 'submissions', label: 'History' },
  ]

  const getDifficultyColor = (diff?: string) => {
    switch (diff?.toLowerCase()) {
      case 'easy': return 'text-green-700 bg-green-100/50 border-green-200'
      case 'medium': return 'text-yellow-700 bg-yellow-100/50 border-yellow-200'
      case 'hard': return 'text-red-700 bg-red-100/50 border-red-200'
      default: return 'text-gray-600 bg-gray-100/50 border-gray-200'
    }
  }

  return (
    <div className="h-full flex flex-col bg-white font-sans">
      {/* Tab Bar */}
      <div className="h-12 shrink-0 flex items-center px-6 border-b border-gray-50 bg-white/80 backdrop-blur sticky top-0 z-20">
        <div className="flex gap-6">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`
                relative text-xs font-bold transition-all py-4 uppercase tracking-wide
                ${activeTab === tab.id 
                  ? 'text-blue-600' 
                  : 'text-gray-400 hover:text-gray-600'
                }
              `}
            >
              {tab.label}
              {activeTab === tab.id && (
                <span className="absolute bottom-0 left-1/2 -translate-x-1/2 w-full h-[3px] bg-blue-600 rounded-t-full shadow-sm" />
              )}
            </button>
          ))}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto custom-scrollbar p-6">
        <div className="max-w-none mx-auto w-full animate-fade-in">
          
          {activeTab === 'description' && (
            <>
              <div className="mb-6">
                <h1 className="text-2xl font-bold text-gray-900 mb-3 leading-tight tracking-tight">
                  {exercise.title}
                </h1>
                <div className="flex items-center gap-3">
                  <span className={`px-3 py-1 rounded-full text-[10px] font-bold uppercase border ${getDifficultyColor(exercise.difficulty)}`}>
                    {exercise.difficulty}
                  </span>
                  <span className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-gray-50 text-gray-500 text-[10px] font-bold uppercase border border-gray-100">
                    <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" /></svg>
                    {exercise.schema.display_name}
                  </span>
                </div>
              </div>

              <div className="prose prose-sm prose-slate max-w-none mb-8">
                <div className="text-gray-600 leading-relaxed whitespace-pre-wrap font-sans text-[15px]">
                  {exercise.description}
                </div>
              </div>

              <div className="p-5 bg-blue-50/50 rounded-3xl border border-blue-100/50 flex gap-4 transition-all hover:bg-blue-50">
                <div className="shrink-0 mt-0.5 w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center">
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h4 className="text-xs font-bold text-blue-800 uppercase tracking-wide mb-1">AI Tutor Hint</h4>
                  <p className="text-sm text-blue-600/90 leading-relaxed">
                    Stuck? Ask the AI assistant on the right to explain the concepts or help debug your query.
                  </p>
                </div>
              </div>
            </>
          )}

          {activeTab === 'solution' && (
            <div className="flex flex-col items-center justify-center py-16 text-center opacity-60">
               <div className="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mb-4 border border-gray-100">
                 <svg className="w-6 h-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                   <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                 </svg>
               </div>
               
               {/* 🔴 Solution 样式 */}
               <h3 className="text-[15px] font-bold text-gray-900 uppercase tracking-wide mb-2">Solution Locked</h3>
               
               <p className="text-sm text-gray-500 max-w-xs mx-auto">
                 Solve the problem correctly to unlock the optimal solution code.
               </p>
            </div>
          )}

          {activeTab === 'submissions' && (
            <div className="flex flex-col items-center justify-center py-16 text-center opacity-60">
              <div className="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mb-4 border border-gray-100">
                 <svg className="w-6 h-6 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                   <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                 </svg>
               </div>
               
              {/* 🔴 改动点：Submissions 样式与 Solution 完全对齐 */}
              <h3 className="text-[15px] font-bold text-gray-900 uppercase tracking-wide mb-2">No History</h3>
              
              <p className="text-sm text-gray-500 max-w-xs mx-auto">
                Run your code to see your submission history here.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}