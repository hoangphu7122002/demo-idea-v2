import AppBar from '@mui/material/AppBar'
import Button from '@mui/material/Button'
import Container from '@mui/material/Container'
import Stack from '@mui/material/Stack'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import { NavLink, Outlet } from 'react-router'
import { ThemeModeToggle } from '../ThemeModeToggle'

const NAV_LINKS = [
  { to: '/notes', label: 'Notes' },
  { to: '/chat', label: 'Chat' },
] as const

export function AppShell() {
  return (
    <>
      <AppBar position="sticky" color="inherit" elevation={0} sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Toolbar sx={{ gap: 3 }}>
          <Typography variant="h6" component="span" sx={{ fontWeight: 800 }}>
            lean-web-stack
          </Typography>
          <Stack component="nav" direction="row" spacing={0.5} sx={{ flexGrow: 1 }} aria-label="Main">
            {NAV_LINKS.map((link) => (
              <Button
                key={link.to}
                component={NavLink}
                to={link.to}
                color="inherit"
                sx={{ '&.active': { color: 'primary.main', bgcolor: 'action.selected' } }}
              >
                {link.label}
              </Button>
            ))}
          </Stack>
          <ThemeModeToggle />
        </Toolbar>
      </AppBar>
      <Container maxWidth="md" component="main" sx={{ py: 4 }}>
        <Outlet />
      </Container>
    </>
  )
}
