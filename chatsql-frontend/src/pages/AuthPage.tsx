import React, { useState, useEffect } from 'react'
import { useAuth } from '../auth/AuthContext'
import { useNavigate, useLocation } from 'react-router-dom'

export default function AuthPage() {
  const { isAuthenticated } = useAuth()
  const { setAuth } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const API_BASE = 'http://127.0.0.1:8000/api/auth'

  const [mode, setMode] = useState<'login' | 'signup'>('login')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [errorMsg, setErrorMsg] = useState('')

  useEffect(() => {
    if (isAuthenticated) {
      const from = (location.state as any)?.from?.pathname || '/'
      navigate(from, { replace: true })
    }
  }, [isAuthenticated, navigate, location])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setErrorMsg('')
    setIsLoading(true)

    // Decide which endpoint to call based on mode
    const url = mode === 'login' ? `${API_BASE}/login/` : `${API_BASE}/signup/`

    console.log('=== AUTH SUBMIT ===')
    console.log('URL =', url, 'mode =', mode)

    try {
      const res = await fetch(url, {
        method: 'POST',
        credentials: 'include', // send cookies for session
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      })

      const data = await res.json()

      if (!res.ok) {
        setErrorMsg(data.error || 'Request failed')
      } else {
        // after signup -> login
        setAuth({
          isAuthenticated: true,
          username: data.username || username,
        })

        // Redirect to home page after successful auth
        navigate('/')
      }
    } catch (err) {
      setErrorMsg('Network error')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.tabs}>
          <button
            style={{
              ...styles.tab,
              ...(mode === 'login' ? styles.active : {}),
            }}
            onClick={() => setMode('login')}
          >
            Login
          </button>
          <button
            style={{
              ...styles.tab,
              ...(mode === 'signup' ? styles.active : {}),
            }}
            onClick={() => setMode('signup')}
          >
            Sign Up
          </button>
        </div>

        <form onSubmit={handleSubmit} style={styles.form}>
          <label style={styles.label}>
            Username
            <input
              style={styles.input}
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </label>

          <label style={styles.label}>
            Password
            <input
              type="password"
              style={styles.input}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>

          {errorMsg && <div style={styles.error}>{errorMsg}</div>}

          <button type="submit" style={styles.button} disabled={isLoading}>
            {isLoading ? 'Submitting...' : mode === 'login' ? 'Login' : 'Create Account'}
          </button>
        </form>
      </div>
    </div>
  )
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    minHeight: '100vh',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    background: '#f5f5f5',
  },
  card: {
    width: '360px',
    padding: '24px',
    borderRadius: '12px',
    background: 'white',
    boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
  },
  tabs: {
    display: 'flex',
    marginBottom: '16px',
  },
  tab: {
    flex: 1,
    padding: '8px 0',
    border: 'none',
    cursor: 'pointer',
    background: 'transparent',
    fontSize: '16px',
    borderBottom: '2px solid transparent',
  },
  active: {
    fontWeight: 'bold',
    borderBottomColor: '#007bff',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '16px',
  },
  label: {
    display: 'flex',
    flexDirection: 'column',
    fontSize: '14px',
    gap: '4px',
  },
  input: {
    padding: '8px 10px',
    borderRadius: '6px',
    border: '1px solid #ccc',
  },
  button: {
    padding: '10px',
    borderRadius: '6px',
    border: 'none',
    background: '#007bff',
    color: 'white',
    cursor: 'pointer',
    fontSize: '15px',
    marginTop: '8px',
  },
  error: {
    color: '#c0392b',
    fontSize: '13px',
  },
}
