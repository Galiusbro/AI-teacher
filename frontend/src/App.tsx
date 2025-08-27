import { BrowserRouter, Routes, Route } from 'react-router-dom'
import RegisterParent from './pages/RegisterParent'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/register/parent" element={<RegisterParent />} />
        <Route path="/" element={<div className="p-4">Home</div>} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
