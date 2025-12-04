import React from 'react'

interface Props { 
  demoOn: boolean
  onToggleDemo: () => void
  onOpenExercises: () => void
}

export default function Header({ demoOn, onToggleDemo, onOpenExercises }: Props){
  return (
    <header className="fixed top-0 left-0 right-0 z-50 h-16 bg-white border-b border-gray-200 px-6 flex items-center justify-between">
      {/* Left: logo + ChatSQL */}
      <div className="flex items-center gap-8">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold text-sm">CS</div>
          <div className="text-xl font-semibold text-gray-900">ChatSQL</div>
        </div>
        
        <button 
          onClick={onOpenExercises}
          className="text-sm text-gray-600 hover:text-gray-900 font-medium"
        >
          Problems
        </button>
      </div>

      {/* Right: Sign in, Sign up, Demo button */}
      <nav className="flex items-center gap-6">
        <a href="#" className="text-sm text-gray-600 hover:text-gray-900">Sign in</a>
        <a href="#" className="text-sm text-gray-600 hover:text-gray-900">Sign up</a>
        <button
          onClick={onToggleDemo}
          aria-pressed={demoOn}
          className={`px-4 py-2 text-sm rounded-md transition-colors ${
            demoOn 
              ? 'bg-blue-600 text-white' 
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          Demo
        </button>
      </nav>
    </header>
  )
}