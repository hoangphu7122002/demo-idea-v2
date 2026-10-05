import { DatePicker, type DatePickerProps } from '@mui/x-date-pickers/DatePicker'
import dayjs from 'dayjs'
import { useController, type Control, type FieldPath, type FieldValues } from 'react-hook-form'

type FormDatePickerProps<T extends FieldValues> = Omit<DatePickerProps, 'name' | 'value' | 'onChange'> & {
  control: Control<T>
  name: FieldPath<T>
  helperText?: string
}

/** MUI date picker bound to React Hook Form. The form value is an ISO date string (`YYYY-MM-DD`) or null. */
export function FormDatePicker<T extends FieldValues>({ control, name, helperText, ...rest }: FormDatePickerProps<T>) {
  const { field, fieldState } = useController({ control, name })
  return (
    <DatePicker
      {...rest}
      value={field.value ? dayjs(field.value) : null}
      onChange={(d) => field.onChange(d && d.isValid() ? d.format('YYYY-MM-DD') : null)}
      inputRef={field.ref}
      slotProps={{
        textField: { name: field.name, onBlur: field.onBlur, error: !!fieldState.error, helperText: fieldState.error?.message ?? helperText },
      }}
    />
  )
}
