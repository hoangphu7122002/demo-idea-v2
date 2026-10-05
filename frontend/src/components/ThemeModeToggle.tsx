import DarkModeIcon from '@mui/icons-material/DarkModeOutlined'
import LightModeIcon from '@mui/icons-material/LightModeOutlined'
import SettingsBrightnessIcon from '@mui/icons-material/SettingsBrightnessOutlined'
import { useColorScheme } from '@mui/material/styles'
import ToggleButton from '@mui/material/ToggleButton'
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup'

type Mode = 'light' | 'dark' | 'system'

/** Light / dark / system. MUI persists the choice to localStorage ("mui-mode"). */
export function ThemeModeToggle() {
  const { mode, setMode } = useColorScheme()
  if (!mode) return null // not resolved yet (first render)
  return (
    <ToggleButtonGroup exclusive size="small" value={mode} aria-label="Theme" onChange={(_e, next: Mode | null) => next && setMode(next)}>
      <ToggleButton value="light" aria-label="Light">
        <LightModeIcon fontSize="small" />
      </ToggleButton>
      <ToggleButton value="dark" aria-label="Dark">
        <DarkModeIcon fontSize="small" />
      </ToggleButton>
      <ToggleButton value="system" aria-label="System">
        <SettingsBrightnessIcon fontSize="small" />
      </ToggleButton>
    </ToggleButtonGroup>
  )
}
