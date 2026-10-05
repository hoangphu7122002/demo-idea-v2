import TextField, { type TextFieldProps } from '@mui/material/TextField'
import { useController, type Control, type FieldPath, type FieldValues } from 'react-hook-form'

type FormTextFieldProps<T extends FieldValues> = Omit<TextFieldProps, 'name' | 'value' | 'onChange' | 'error'> & {
  control: Control<T>
  name: FieldPath<T>
}

/** MUI TextField bound to React Hook Form: value, onChange and the Zod error message come from the form. */
export function FormTextField<T extends FieldValues>({ control, name, helperText, ...rest }: FormTextFieldProps<T>) {
  const { field, fieldState } = useController({ control, name })
  return (
    <TextField
      {...rest}
      {...field}
      value={field.value ?? ''}
      error={!!fieldState.error}
      helperText={fieldState.error?.message ?? helperText}
    />
  )
}
