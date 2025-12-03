import React, { createContext, useContext, useEffect, useState } from 'react'

type AuthContextValue = {
  isLoading: boolean
  isAuthenticated: boolean
  username: string | null
  refreshMe: () => Promise<void>
  setAuth: (opts: { isAuthenticated: boolean; username: string | null }) => void
}

const API_BASE = 'http://127.0.0.1:8000/api/auth'

// create context object
const AuthContext = createContext<AuthContextValue | undefined>(undefined)

// AuthProvider
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // isLoading
  const [isLoading, setIsLoading] = useState(true)

  // logged in
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  // username (null if not logged in)
  const [username, setUsername] = useState<string | null>(null)

  const refreshMe = async () => {
    try {
      setIsLoading(true) // ✔ ensure loading state resets

      const res = await fetch(`${API_BASE}/me/`, {
        method: 'GET',
        credentials: 'include', // important for session cookie
      })

      if (!res.ok) {
        // not logged in
        setIsAuthenticated(false)
        setUsername(null)
        return
      }

      const data = await res.json()

      // case 1: backend returns { authenticated: true/false, username: ... }
      if (typeof data.authenticated === 'boolean') {
        if (data.authenticated) {
          setIsAuthenticated(true)
          setUsername(data.username || null)
        } else {
          setIsAuthenticated(false)
          setUsername(null)
        }
        return // stop here if backend provides `authenticated`
      }

      // case 2: no "authenticated" field, fall back to username
      if (data.username) {
        setIsAuthenticated(true)
        setUsername(data.username)
      } else {
        setIsAuthenticated(false)
        setUsername(null)
      }
    } catch (err) {
      // on error, treat as not authenticated
      setIsAuthenticated(false)
      setUsername(null)
    } finally {
      setIsLoading(false)
    }
  }

  // Run refreshMe() ONCE when the app first loads.
  useEffect(() => {
    refreshMe()
  }, [])

  // setAuth() is used right after login() or logout().
  const setAuth = (opts: { isAuthenticated: boolean; username: string | null }) => {
    setIsAuthenticated(opts.isAuthenticated)
    setUsername(opts.username)
  }

  return (
    <AuthContext.Provider
      value={{
        isLoading,
        isAuthenticated,
        username,
        refreshMe,
        setAuth,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

// components can easily access auth state.
export const useAuth = (): AuthContextValue => {
  const ctx = useContext(AuthContext)
  if (!ctx) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return ctx
}
