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

  if (isLoading) {
    return <div className="text-center text-gray-500">Loading...</div>
  }

  return (
    <div className="space-y-3">
      {exercises.map((ex, index) => (
        <div
          key={ex.id}
          role="button"
          tabIndex={0}
          aria-pressed={selectedId === ex.id}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') onSelect(ex.id)
          }}
          onClick={() => onSelect(ex.id)}
          className={`p-4 rounded-xl border-2 transition-all cursor-pointer ${
            selectedId === ex.id
              ? 'border-blue-500 bg-blue-50 shadow-md'
              : 'border-gray-200 hover:border-gray-300 hover:shadow-sm hover:bg-gray-50'
          }`}
        >
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-3">
              <span className="text-sm font-medium text-gray-500">{index + 1}.</span>
              <div className="text-base font-semibold text-gray-900">{ex.title}</div>
            </div>
            <span className="text-xs px-2 py-1 rounded-md bg-gray-100 text-gray-600">
              {ex.difficulty}
            </span>
          </div>
          <div className="text-sm text-gray-600 ml-7">{ex.schema.display_name}</div>
        </div>
      ))}
    </div>
  )
}
