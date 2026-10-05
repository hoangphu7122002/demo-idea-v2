import { render } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import type { ReactElement } from 'react'
import { createMemoryRouter, RouterProvider } from 'react-router'
import { AppProviders } from '../app/AppProviders'
import { routes } from '../app/router'
import { makeStore, type AppStore } from '../app/store'

/** Render one component with the real theme, store, snackbars and date adapter. A fresh store per test. */
export function renderWithProviders(ui: ReactElement, { store = makeStore() }: { store?: AppStore } = {}) {
  return { store, user: userEvent.setup(), ...render(<AppProviders store={store}>{ui}</AppProviders>) }
}

/** Render the whole app at `path` with an in-memory router (for page and navigation tests). */
export function renderApp(path = '/', options: { store?: AppStore } = {}) {
  const router = createMemoryRouter(routes, { initialEntries: [path] })
  return { router, ...renderWithProviders(<RouterProvider router={router} />, options) }
}
