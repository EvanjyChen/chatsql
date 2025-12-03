import React, { useState, useEffect } from 'react'
import { getExercises } from '../services/api'
import type { Exercise as Ex } from '../types'

interface Props {
  selectedId: number | null
  onSelect: (id: number) => void
  demoMode: boolean
}

export default function ProblemList({ selectedId, onSelect, demoMode }: Props) {
  const [exercises, setExercises] = useState<Ex[]>([])
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    loadExercises()
  }, [demoMode])

  async function loadExercises() {
    try {
      setIsLoading(true)
      const ex = await getExercises(demoMode)
      setExercises(ex)
    } catch (e) {
      console.error(e)
    } finally {
      setIsLoading(false)
    }
  }

  // 辅助函数：难度颜色
  const getDifficultyColor = (diff?: string) => {
    switch (diff?.toLowerCase()) {
      case 'easy': return 'bg-green-100 text-green-700'
      case 'medium': return 'bg-yellow-100 text-yellow-700'
      case 'hard': return 'bg-red-100 text-red-700'
      default: return 'bg-gray-100 text-gray-600'
    }
  }

  if (isLoading) {
    return (
      <div className="space-y-3 px-2">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-20 bg-gray-200 rounded-xl animate-pulse"></div>
        ))}
      </div>
    )
  }

  return (
    <div className="space-y-1">
      {exercises.map((ex, index) => {
        const isSelected = selectedId === ex.id
        return (
          <div
            key={ex.id}
            onClick={() => onSelect(ex.id)}
            className={`
              group relative flex items-center justify-between p-4 rounded-xl cursor-pointer transition-all duration-200 border
              ${isSelected 
                ? 'bg-white border-blue-200 shadow-sm ring-1 ring-blue-100' 
                : 'bg-white border-transparent hover:bg-white hover:shadow-sm hover:border-gray-200'
              }
            `}
          >
            <div className="flex items-center gap-4">
              {/* Index Number Circle */}
              <div className={`
                w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-colors
                ${isSelected ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-500 group-hover:bg-gray-200'}
              `}>
                {index + 1}
              </div>

              {/* Title & Schema */}
              <div>
                <h3 className={`text-sm font-semibold ${isSelected ? 'text-blue-900' : 'text-gray-900'}`}>
                  {ex.title}
                </h3>
                <p className="text-xs text-gray-500 flex items-center gap-1.5 mt-0.5">
                  <svg className="w-3 h-3 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
                  </svg>
                  {ex.schema.display_name}
                </p>
              </div>
            </div>

            {/* Right Side: Badge & Arrow */}
            <div className="flex items-center gap-4">
              <span className={`px-2.5 py-1 rounded-md text-[10px] font-bold uppercase tracking-wider ${getDifficultyColor(ex.difficulty)}`}>
                {ex.difficulty}
              </span>
              
              {/* Chevron Icon (iOS style) */}
              <svg 
                className={`w-5 h-5 transition-transform ${isSelected ? 'text-blue-500 translate-x-1' : 'text-gray-300 group-hover:text-gray-400'}`} 
                fill="none" viewBox="0 0 24 24" stroke="currentColor"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </div>
        )
      })}
    </div>
  )
}