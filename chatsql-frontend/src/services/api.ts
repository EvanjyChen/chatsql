import axios from 'axios'
import type { DatabaseSchema, Exercise, QueryResult, SubmitResult, AIResponse } from '../types'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: false,
})


// --- Mock data ---
const mockSchemas: DatabaseSchema[] = [
  { id: 1, name: 'employees', display_name: 'Employees DB', description: 'Demo employees schema', exercise_count: 3 }
]

const mockExercises: Exercise[] = [
  {
    id: 1,
    title: 'Two Sum (SQL demo)',
    description: 'Find pairs of employees in the same department.',
    difficulty: 'easy',
    initial_query: 'SELECT id, name, dept FROM employees',
    hints: [{ level: 1, text: 'Start with a simple SELECT' }],
    schema: { id: 1, name: 'employees', display_name: 'Employees DB', db_name: 'employees' },
    tags: ['select', 'join']
  },
  {
    id: 2,
    title: 'Count by Department',
    description: 'Count number of employees per department.',
    difficulty: 'easy',
    initial_query: 'SELECT dept, COUNT(*) FROM employees GROUP BY dept',
    hints: [],
    schema: { id: 1, name: 'employees', display_name: 'Employees DB', db_name: 'employees' },
    tags: ['aggregate']
  },
  {
    id: 3,
    title: 'Top Salaries',
    description: 'Find employees with highest salaries in each department.',
    difficulty: 'medium',
    initial_query: 'SELECT * FROM employees',
    hints: [],
    schema: { id: 1, name: 'employees', display_name: 'Employees DB', db_name: 'employees' },
    tags: ['window', 'join']
  }
]

const mockQueryResult: QueryResult = {
  success: true,
  columns: ['id', 'name', 'dept'],
  rows: [[1, 'Alice', 'Engineering'], [2, 'Bob', 'Engineering'], [3, 'Carol', 'HR']],
  row_count: 3,
  execution_time: 12,
}

const mockSubmitResult: SubmitResult = {
  correct: true,
  message: 'All tests passed (mock).',
  user_result: mockQueryResult,
}

const mockAIResponse: AIResponse = { response: 'This is a mocked AI response. Try selecting fewer columns.' }

// --- Helpers ---
async function tryApi<T>(fn: () => Promise<T>, fallback: T, useMock: boolean): Promise<T> {
  if (useMock) return Promise.resolve(fallback)
  try {
    return await fn()
  } catch (e) {
    console.warn('API unavailable, falling back to mock data', e)
    return fallback
  }
}

export const getSchemas = async (useMock = false): Promise<DatabaseSchema[]> => {
  return tryApi(async () => {
    const r = await api.get('/schemas/')
    return r.data
  }, mockSchemas, useMock)
}

export const getExercises = async (useMock = false, params?: any): Promise<Exercise[]> => {
  return tryApi(async () => {
    const r = await api.get('/exercises/', { params })
    return r.data
  }, mockExercises, useMock)
}

export const getExercise = async (id: number, useMock = false): Promise<Exercise> => {
  return tryApi(async () => {
    const r = await api.get(`/exercises/${id}/`)
    return r.data
  }, mockExercises.find(e => e.id === id) || mockExercises[0], useMock)
}

export const executeQuery = async (exerciseId: number, query: string, useMock = false): Promise<QueryResult> => {
  return tryApi(async () => {
    const r = await api.post(`/exercises/${exerciseId}/execute/`, { query })
    return r.data
  }, { ...mockQueryResult, rows: mockQueryResult.rows }, useMock)
}

export const submitQuery = async (exerciseId: number, query: string, useMock = false): Promise<SubmitResult> => {
  return tryApi(async () => {
    const r = await api.post(`/exercises/${exerciseId}/submit/`, { query })
    return r.data
  }, mockSubmitResult, useMock)
}

export const getAIResponse = async (exerciseId: number, message: string, userQuery?: string, error?: string, useMock = false): Promise<AIResponse> => {
  return tryApi(async () => {
    const r = await api.post(`/exercises/${exerciseId}/ai/`, { message, user_query: userQuery, error })
    return r.data
  }, mockAIResponse, useMock)
}

export default api