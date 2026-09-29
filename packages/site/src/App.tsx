import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './routes/HomePage'
import TasksPage from './routes/TasksPage'
import TaskDetailPage from './routes/TaskDetailPage'
import SubmissionPage from './routes/SubmissionPage'
import ComparePage from './routes/ComparePage'
import ProposeTaskPage from './routes/ProposeTaskPage'
import AboutPage from './routes/AboutPage'

export default function App() {
  return (
    <BrowserRouter basename={import.meta.env.BASE_URL}>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/tasks" element={<TasksPage />} />
          <Route path="/tasks/:taskId" element={<TaskDetailPage />} />
          <Route path="/tasks/:taskId/submissions/:participantId" element={<SubmissionPage />} />
          <Route path="/compare/:taskId" element={<ComparePage />} />
          <Route path="/propose" element={<ProposeTaskPage />} />
          <Route path="/about" element={<AboutPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
