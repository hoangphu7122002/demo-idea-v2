import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import tseslint from 'typescript-eslint'

// MUI v9 removed these props. AI assistants and old docs still suggest them. See frontend/CLAUDE.md.
const REMOVED_MUI_PROPS = {
  InputProps: 'slotProps={{ input: ... }}',
  inputProps: 'slotProps={{ htmlInput: ... }} (on TextField)',
  InputLabelProps: 'slotProps={{ inputLabel: ... }}',
  FormHelperTextProps: 'slotProps={{ formHelperText: ... }}',
  SelectProps: 'slotProps={{ select: ... }}',
  PaperProps: 'slotProps={{ paper: ... }}',
  BackdropProps: 'slotProps={{ backdrop: ... }}',
  MenuListProps: 'slotProps={{ list: ... }}',
  ListboxProps: 'slotProps={{ listbox: ... }}',
  PopperProps: 'slotProps={{ popper: ... }}',
  TransitionComponent: 'slots={{ transition: ... }}',
  TransitionProps: 'slotProps={{ transition: ... }}',
  componentsProps: 'slotProps',
  primaryTypographyProps: 'slotProps={{ primary: ... }}',
  secondaryTypographyProps: 'slotProps={{ secondary: ... }}',
}

const RAW_COLOUR = '/^(#[0-9a-fA-F]{3,8}|(rgb|hsl)a?\\(.*)$/'

const muiRules = [
  ...Object.entries(REMOVED_MUI_PROPS).map(([prop, fix]) => ({
    selector: `JSXAttribute[name.name='${prop}']`,
    message: `${prop} was removed in MUI v9. Use ${fix}.`,
  })),
  { selector: "JSXOpeningElement[name.name='Grid'] > JSXAttribute[name.name='item']", message: 'Grid has no `item` in MUI v9. Use size={{ xs: 12, md: 6 }}.' },
  { selector: "JSXAttribute[name.name='style']", message: 'Use the sx prop with theme tokens, not style.' },
  { selector: `Literal[value=${RAW_COLOUR}]`, message: 'Raw colour. Add it to src/app/theme.ts and use a palette token (e.g. "primary.main").' },
  { selector: `TemplateElement[value.raw=${RAW_COLOUR}]`, message: 'Raw colour. Add it to src/app/theme.ts and use a palette token.' },
]

export default tseslint.config(
  { ignores: ['dist', 'src/api/schema.d.ts'] },
  {
    extends: [js.configs.recommended, ...tseslint.configs.recommended],
    files: ['**/*.{ts,tsx}'],
    languageOptions: { ecmaVersion: 2023, globals: globals.browser },
    plugins: { 'react-hooks': reactHooks, 'react-refresh': reactRefresh },
    rules: {
      ...reactHooks.configs.recommended.rules,
      'react-refresh/only-export-components': ['warn', { allowConstantExport: true }],
    },
  },
  {
    files: ['src/**/*.{ts,tsx}'],
    ignores: ['src/app/theme.ts'],
    rules: {
      'no-restricted-syntax': ['error', ...muiRules],
      'no-restricted-imports': [
        'error',
        {
          paths: [
            { name: '@mui/material', message: "Import per component: import Button from '@mui/material/Button'." },
            { name: '@mui/icons-material', message: "Import per icon: import SendIcon from '@mui/icons-material/Send'." },
          ],
        },
      ],
    },
  },
)
