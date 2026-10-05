import CssBaseline from '@mui/material/CssBaseline'
import { ThemeProvider } from '@mui/material/styles'
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import { SnackbarProvider } from 'notistack'
import type { ReactNode } from 'react'
import { Provider } from 'react-redux'
import type { AppStore } from './store'
import { theme } from './theme'

/** Every non-routing provider the app needs; shared by main.tsx and tests (`src/test/render.tsx`). */
export function AppProviders({ store, children }: { store: AppStore; children: ReactNode }) {
  return (
    <Provider store={store}>
      <ThemeProvider theme={theme} defaultMode="system">
        <CssBaseline enableColorScheme />
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <SnackbarProvider maxSnack={3} autoHideDuration={3000} anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}>
            {children}
          </SnackbarProvider>
        </LocalizationProvider>
      </ThemeProvider>
    </Provider>
  )
}
