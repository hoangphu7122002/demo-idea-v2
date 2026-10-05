import { createTheme } from '@mui/material/styles'

/**
 * The single source of colours, spacing, shape, typography and component defaults.
 * Raw colours (hex, rgb, hsl) are only allowed in this file; eslint blocks them elsewhere.
 * Use palette tokens in components: `color="primary"`, `sx={{ bgcolor: 'background.paper' }}`.
 */
export const theme = createTheme({
  cssVariables: { colorSchemeSelector: 'class' },
  colorSchemes: {
    light: {
      palette: {
        primary: { main: '#4f46e5' },
        secondary: { main: '#0891b2' },
        background: { default: '#f7f7fb', paper: '#ffffff' },
      },
    },
    dark: {
      palette: {
        primary: { main: '#a5b4fc' },
        secondary: { main: '#67e8f9' },
        background: { default: '#0f1117', paper: '#171a23' },
      },
    },
  },
  shape: { borderRadius: 10 },
  typography: {
    fontFamily: 'system-ui, -apple-system, "Segoe UI", Roboto, sans-serif',
    button: { textTransform: 'none', fontWeight: 600 },
  },
  components: {
    MuiButton: { defaultProps: { disableElevation: true } },
    MuiChip: { defaultProps: { size: 'small' } },
    MuiPaper: { defaultProps: { variant: 'outlined' } },
    MuiTextField: { defaultProps: { size: 'small', fullWidth: true } },
    MuiDialog: { defaultProps: { fullWidth: true, maxWidth: 'sm' } },
  },
})
