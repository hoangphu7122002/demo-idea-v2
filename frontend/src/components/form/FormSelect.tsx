import MenuItem from '@mui/material/MenuItem'
import TextField, { type TextFieldProps } from '@mui/material/TextField'
import { useController, type Control, type FieldPath, type FieldValues } from 'react-hook-form'

export interface SelectOption {
  value: string
  label: string
}

type FormSelectProps<T extends FieldValues> = Omit<TextFieldProps, 'name' | 'value' | 'onChange' | 'error' | 'select'> & {
  control: Control<T>
  name: FieldPath<T>
  options: readonly SelectOption[]
  /** Adds an option for the empty value, e.g. "Any". */
  emptyOptionLabel?: string
}

/** MUI select bound to React Hook Form. */
export function FormSelect<T extends FieldValues>({ control, name, options, emptyOptionLabel, helperText, ...rest }: FormSelectProps<T>) {
  const { field, fieldState } = useController({ control, name })
  return (
    <TextField
      {...rest}
      {...field}
      select
      value={field.value ?? ''}
      error={!!fieldState.error}
      helperText={fieldState.error?.message ?? helperText}
    >
      {emptyOptionLabel !== undefined && (
        <MenuItem value="">
          <em>{emptyOptionLabel}</em>
        </MenuItem>
      )}
      {options.map((o) => (
        <MenuItem key={o.value} value={o.value}>
          {o.label}
        </MenuItem>
      ))}
    </TextField>
  )
}
