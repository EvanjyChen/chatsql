import React, { useState, useEffect, useRef } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

interface Props {
  demoOn: boolean
  onToggleDemo: () => void
  onOpenExercises: () => void
}

export default function Header({ demoOn, onToggleDemo, onOpenExercises }: Props) {
  const { isLoading, isAuthenticated, username, refreshMe } = useAuth()
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const menuRef = useRef<HTMLDivElement | null>(null)
  const API_BASE = 'http://127.0.0.1:8000/api/auth'

  // get the first letter of username, uppercased
  const initial = username && username.length > 0 ? username.charAt(0).toUpperCase() : '?'

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (!menuRef.current) return
      if (!menuRef.current.contains(event.target as Node)) {
        setIsMenuOpen(false)
      }
    }

    if (isMenuOpen) {
      document.addEventListener('mousedown', handleClickOutside)
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [isMenuOpen])

  const handleLogout = async () => {
    try {
      await fetch(`${API_BASE}/logout/`, {
        method: 'POST',
        credentials: 'include', // send cookies so server can clear session
      })
    } catch (err) {
      // Even if the request fails, we still want to refresh auth state
    } finally {
      await refreshMe()
      setIsMenuOpen(false)
    }
  }

  console.log('Header auth state:', {
    isLoading,
    isAuthenticated,
    username,
  })

  return (
    <header className="fixed top-0 left-0 right-0 z-50 h-16 bg-white border-b border-gray-200 px-6 flex items-center justify-between">
      {/* Left: ChatSQL */}
      <div className="flex items-center gap-8">
        <div className="text-xl font-semibold text-gray-900">ChatSQL</div>

        <button
          onClick={onOpenExercises}
          className="text-sm text-gray-600 hover:text-gray-900 font-medium"
        >
          Problems
        </button>
      </div>

      {/* Right side: auth area + Demo button */}
      <nav className="flex items-center gap-6">
        {/* Auth area: show sign buttons OR profile circle */}
        {!isAuthenticated && (
          <>
            <Link to="/auth" className="text-sm text-gray-600 hover:text-gray-900">
              Sign in
            </Link>
            <Link to="/auth" className="text-sm text-gray-600 hover:text-gray-900">
              Sign up
            </Link>
          </>
        )}

        {isAuthenticated && (
          <div ref={menuRef} className="relative">
            {/* Profile circle button */}
            <button
              type="button"
              onClick={() => setIsMenuOpen((open) => !open)}
              className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-sm font-semibold text-gray-700"
            >
              {initial}
            </button>

            {/* Simple dropdown menu */}
            {isMenuOpen && (
              <div className="absolute right-0 mt-2 w-32 bg-white border border-gray-200 rounded-md shadow-lg py-1 text-sm">
                <div className="px-3 py-1 text-gray-500 border-b border-gray-100">{username}</div>
                <button
                  type="button"
                  onClick={handleLogout}
                  className="w-full text-left px-3 py-2 hover:bg-gray-100 text-gray-800"
                >
                  Logout
                </button>
              </div>
            )}
          </div>
        )}

        {/* Demo toggle button (always visible) */}
        <button
          onClick={onToggleDemo}
          aria-pressed={demoOn}
          className={`px-4 py-2 text-sm rounded-md transition-colors ${
            demoOn ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
          }`}
        >
          Demo
        </button>
      </nav>
    </header>
  )
}
