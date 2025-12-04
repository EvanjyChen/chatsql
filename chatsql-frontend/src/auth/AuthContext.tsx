import React, { createContext, useContext, useEffect, useState } from 'react'

// 1. 定义类型：增加了 role
type AuthContextValue = {
  isLoading: boolean
  isAuthenticated: boolean
  username: string | null
  role: 'student' | 'instructor' | null // 🟢 新增 role 字段
  refreshMe: () => Promise<void>
  setAuth: (opts: { 
    isAuthenticated: boolean; 
    username: string | null; 
    role: 'student' | 'instructor' | null 
  }) => void
}

const API_BASE = 'http://127.0.0.1:8000/api/auth'

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isLoading, setIsLoading] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [username, setUsername] = useState<string | null>(null)
  const [role, setRole] = useState<'student' | 'instructor' | null>(null) // 🟢 新增 role 状态

  const refreshMe = async () => {
    try {
      setIsLoading(true)

      const res = await fetch(`${API_BASE}/me/`, {
        method: 'GET',
        credentials: 'include', // 携带 Cookie
      })

      if (!res.ok) {
        setIsAuthenticated(false)
        setUsername(null)
        setRole(null)
        return
      }

      const data = await res.json()

      // 假设后端 /me/ 接口也会返回 { username: "...", role: "..." }
      // 如果后端还没更新 /me/ 接口，默认 fallback 到 'student' 防止报错
      const userRole = data.role || 'student'

      if (data.username || data.authenticated) {
        setIsAuthenticated(true)
        setUsername(data.username)
        setRole(userRole) // 🟢 恢复会话时设置 role
      } else {
        setIsAuthenticated(false)
        setUsername(null)
        setRole(null)
      }
    } catch (err) {
      setIsAuthenticated(false)
      setUsername(null)
      setRole(null)
    } finally {
      setIsLoading(false)
    }
  }

  // 初始化时检查一次登录状态
  useEffect(() => {
    refreshMe()
  }, [])

  // 登录或登出时调用
  const setAuth = (opts: { 
    isAuthenticated: boolean; 
    username: string | null; 
    role: 'student' | 'instructor' | null 
  }) => {
    setIsAuthenticated(opts.isAuthenticated)
    setUsername(opts.username)
    setRole(opts.role)
  }

  return (
    <AuthContext.Provider
      value={{
        isLoading,
        isAuthenticated,
        username,
        role,
        refreshMe,
        setAuth,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = (): AuthContextValue => {
  const ctx = useContext(AuthContext)
  if (!ctx) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return ctx
}