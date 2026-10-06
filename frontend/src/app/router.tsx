import LinearProgress from '@mui/material/LinearProgress'
import { createBrowserRouter, Navigate, type RouteObject } from 'react-router'
import { AppShell } from '../components/layout/AppShell'
import { NotFoundPage } from '../pages/NotFoundPage'

// Each page is lazy-loaded into its own chunk; the shell ships in the entry chunk.
export const routes: RouteObject[] = [
  {
    element: <AppShell />,
    // Shown while the first page's chunk loads.
    hydrateFallbackElement: <LinearProgress aria-label="Loading page" />,
    children: [
      { index: true, element: <Navigate to="/notes" replace /> },
      { path: 'notes', lazy: () => import('../pages/NotesPage').then((m) => ({ Component: m.NotesPage })) },
      { path: 'chat', lazy: () => import('../pages/ChatPage').then((m) => ({ Component: m.ChatPage })) },
      { path: 'posts/:slug', lazy: () => import('../pages/PostPage').then((m) => ({ Component: m.PostPage })) },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
]

export const createAppRouter = () => createBrowserRouter(routes)
