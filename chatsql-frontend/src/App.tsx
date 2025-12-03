import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

import Layout from './components/Layout'
import AuthPage from './pages/AuthPage'
import { AuthProvider } from './auth/AuthContext'
import ProtectedRoute from './auth/ProtectedRoute'

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public homepage */}
          <Route path="/" element={<Layout />} />

          {/* Public login/signup page */}
          <Route path="/auth" element={<AuthPage />} />

          {/* ProtectedRoute */}
          {/*
          <Route
            path="/chat"
            element={
              <ProtectedRoute>
                <ChatPage />
              </ProtectedRoute>
            }
          />
          */}
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}
