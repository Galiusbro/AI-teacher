import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import RegisterParent from './pages/RegisterParent'
import RegisterStudent from './pages/RegisterStudent'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import ParentDashboard from './pages/ParentDashboard'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/register/parent" element={<RegisterParent />} />
        <Route path="/register/student" element={<RegisterStudent />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/dashboard/:role" element={<Dashboard />} />
        <Route path="/parent/dashboard" element={<ParentDashboard />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
