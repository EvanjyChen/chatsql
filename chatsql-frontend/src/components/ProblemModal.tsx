import React from 'react'
import ProblemList from './ProblemList'

interface Props {
  isOpen: boolean
  onClose: () => void
  selectedId: number | null
  onSelect: (id: number) => void
  demoMode: boolean
}

export default function ProblemModal({ isOpen, onClose, selectedId, onSelect, demoMode }: Props) {
  if (!isOpen) return null

  const handleSelect = (id: number) => {
    onSelect(id)
    onClose()
  }

  const handleRandom = () => {
    // TODO: implement with actual exercise count
    const randomId = Math.floor(Math.random() * 3) + 1
    handleSelect(randomId)
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      onClick={onClose}
    >
      <div
        className="bg-white rounded-xl shadow-2xl w-full max-w-3xl mx-4 max-h-[80vh] flex flex-col"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <h2 className="text-2xl font-semibold text-gray-900">Problem List</h2>
          <div className="flex items-center gap-3">
            <button
              onClick={handleRandom}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
            >
              Random
            </button>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-gray-600 text-2xl leading-none w-8 h-8 flex items-center justify-center"
              aria-label="Close"
            >
              ×
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="overflow-auto p-6">
          <ProblemList selectedId={selectedId} onSelect={handleSelect} demoMode={demoMode} />
        </div>
      </div>
    </div>
  )
}