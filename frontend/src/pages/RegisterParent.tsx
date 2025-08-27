import { useState } from 'react'
import axios from 'axios'
import api from '../services/api'

interface ParentForm {
  email: string
  password: string
  locale: string
}

interface RegisterResponse {
  user_id: string
  role: string
}

export default function RegisterParent() {
  const [form, setForm] = useState<ParentForm>({ email: '', password: '', locale: 'ru' })
  const [result, setResult] = useState<RegisterResponse | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const response = await api.post<RegisterResponse>('/register/parent', form)
      setResult(response.data)
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        setError(err.response?.data?.message || 'Registration failed')
      } else {
        setError('Registration failed')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-md mx-auto mt-10 p-4">
      <h2 className="text-2xl font-bold mb-4">Parent Registration</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="email"
          name="email"
          value={form.email}
          onChange={handleChange}
          required
          placeholder="Email"
          className="w-full border p-2 rounded"
        />
        <input
          type="password"
          name="password"
          value={form.password}
          onChange={handleChange}
          required
          placeholder="Password"
          className="w-full border p-2 rounded"
        />
        <input
          type="text"
          name="locale"
          value={form.locale}
          onChange={handleChange}
          placeholder="Locale (e.g. ru)"
          className="w-full border p-2 rounded"
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-500 text-white py-2 rounded disabled:opacity-50"
        >
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>
      {result && (
        <div className="mt-4 text-green-600">
          Registered user {result.user_id} as {result.role}
        </div>
      )}
      {error && (
        <div className="mt-4 text-red-600">
          {error}
        </div>
      )}
    </div>
  )
}
