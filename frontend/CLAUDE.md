# Frontend rules

Full guide for humans: `docs/playbooks/09-frontend-ui.md`.

## Stack

MUI v9 + Emotion · MUI X Date Pickers + dayjs · Redux Toolkit + RTK Query · React Router v7 · React Hook Form + Zod · notistack · openapi-fetch typed client (`src/api/`, generated) · vitest + Testing Library + user-event.

## Rules

- Reuse first: check `src/components/`, `src/components/form/`, `src/hooks/` before writing UI or submit logic.
- MUI components only. Shared UI in `src/components/`; feature code in `src/features/<feature>/`; one page per route in `src/pages/`.
- Style only with `sx` and theme tokens (`'primary.main'`, `'text.secondary'`, `'divider'`, spacing numbers). No `style` prop, no CSS files, no hex/rgb/hsl outside `src/app/theme.ts`.
- New colour or app-wide default → `src/app/theme.ts` (both `colorSchemes.light` and `.dark`, or `components.Mui*.defaultProps`).
- Import per component/icon: `import Button from '@mui/material/Button'`, `import AddIcon from '@mui/icons-material/Add'`.
- Server data: RTK Query endpoints in `features/<f>/<f>Api.ts` via `baseApi.injectEndpoints`, `queryFn: () => fromApi(() => api.GET(...))`. Add tags to `tagTypes` in `src/services/baseApi.ts`. Never `useEffect` + `fetch`, never server data in a slice.
- Render query results with `QueryState`. Run mutations with `useMutationToast`.
- Redux slices only for client state shared across components (filters, selection). Register in `src/app/store.ts`; use `useAppSelector` / `useAppDispatch`.
- New page: `src/pages/XPage.tsx` + lazy route in `src/app/router.tsx` + `NAV_LINKS` in `components/layout/AppShell.tsx`.
- Forms: Zod schema in `<thing>Schema.ts` → `useForm({ resolver: zodResolver(schema) })` → `FormTextField` / `FormSelect` / `FormDatePicker`, inside `FormDialog`. New input type → `src/components/form/Form<Thing>.tsx` with `useController`.
- Value → label/colour maps live in one `*Meta.ts` per feature (see `features/notes/noteMeta.ts`).
- Tests: `renderWithProviders` (component) or `renderApp(path)` (page/flow) from `src/test/render.tsx`; mock `api.GET` / `api.POST` with `vi.spyOn`; query by role/name.
- Check new screens in light and dark mode.

## MUI v9: props that no longer exist (your training data still has them)

| Removed | Use |
|---|---|
| `InputProps` | `slotProps={{ input: ... }}` |
| `inputProps` (TextField) | `slotProps={{ htmlInput: ... }}` |
| `InputLabelProps` | `slotProps={{ inputLabel: ... }}` |
| `FormHelperTextProps` | `slotProps={{ formHelperText: ... }}` |
| `SelectProps` | `slotProps={{ select: ... }}` |
| `PaperProps`, `BackdropProps`, `MenuListProps`, `ListboxProps`, `PopperProps` | `slotProps={{ paper / backdrop / list / listbox / popper }}` |
| `TransitionComponent`, `TransitionProps` | `slots={{ transition }}`, `slotProps={{ transition }}` |
| `componentsProps`, `components` | `slotProps`, `slots` |
| `primaryTypographyProps`, `secondaryTypographyProps` | `slotProps={{ primary / secondary }}` |
| `<Grid item xs={6}>` | `<Grid size={{ xs: 6 }}>` |
| `LoadingButton` (lab) | `<Button loading>` |
| DatePicker `renderInput` | `slotProps={{ textField: ... }}` |

## Before finishing

`npm run lint && npm run typecheck && npm test` (or `make check` from the root).
