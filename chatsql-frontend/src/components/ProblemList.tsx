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
  const [difficulty, setDifficulty] = useState<string>('')
  const [search, setSearch] = useState<string>('')

  useEffect(() => {
    loadExercises()
  }, [demoMode, difficulty, search])

  async function loadExercises() {
    try {
      setIsLoading(true)
      const params: any = {}
      if (difficulty) params.difficulty = difficulty
      if (search) params.search = search
      const ex = await getExercises(demoMode, params)
      // 确保按照 order 字段排序（从小到大），order 相同时按 id 排序
      const sorted = [...ex].sort((a, b) => {
        const orderA = a.order ?? 999999  // 如果没有 order，放在最后
        const orderB = b.order ?? 999999
        if (orderA !== orderB) {
          return orderA - orderB
        }
        return a.id - b.id
      })
      setExercises(sorted)
    } catch (e) {
      console.error(e)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="space-y-4">
      {/* 筛选器 */}
      <div className="flex flex-wrap items-center gap-3">
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">Difficulty</label>
          <select
            className="border border-gray-300 rounded-md px-2 py-1 text-sm"
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
          >
            <option value="">All</option>
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>
        </div>

        <div className="flex-1 min-w-[120px]">
          <label className="block text-xs font-medium text-gray-500 mb-1">Search</label>
          <input
            type="text"
            className="w-full border border-gray-300 rounded-md px-2 py-1 text-sm"
            placeholder="Search by title / description / tag"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      {/* 题目列表 */}
      <div className="space-y-3">
        {isLoading && (
          <div className="text-xs text-gray-400">Loading...</div>
        )}
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
            <div className="text-sm text-gray-600 ml-7">
              {typeof ex.schema === 'string' ? ex.schema : ex.schema.display_name}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}