import { zodResolver } from '@hookform/resolvers/zod'
import { screen, within } from '@testing-library/react'
import { useForm } from 'react-hook-form'
import { expect, test, vi } from 'vitest'
import { z } from 'zod'
import { renderWithProviders } from '../../test/render'
import { FormDatePicker } from './FormDatePicker'
import { FormSelect } from './FormSelect'

const schema = z.object({ colour: z.string().min(1, 'Pick a colour'), due: z.string().nullable() })
type Values = z.infer<typeof schema>

function Demo({ onValid }: { onValid: (v: Values) => void }) {
  const { control, handleSubmit } = useForm<Values>({ resolver: zodResolver(schema), defaultValues: { colour: '', due: '2026-10-03' } })
  return (
    <form onSubmit={handleSubmit(onValid)} noValidate>
      <FormSelect control={control} name="colour" label="Colour" options={[{ value: 'blue', label: 'Blue' }]} />
      <FormDatePicker control={control} name="due" label="Due" />
      <button type="submit">Save</button>
    </form>
  )
}

test('FormSelect shows the Zod error, then submits the chosen value with the date', async () => {
  const onValid = vi.fn()
  const { user } = renderWithProviders(<Demo onValid={onValid} />)
  await user.click(screen.getByRole('button', { name: 'Save' }))
  expect(await screen.findByText('Pick a colour')).toBeTruthy()

  await user.click(screen.getByRole('combobox', { name: /colour/i }))
  await user.click(within(await screen.findByRole('listbox')).getByRole('option', { name: 'Blue' }))
  await user.click(screen.getByRole('button', { name: 'Save' }))
  expect(onValid.mock.calls[0][0]).toEqual({ colour: 'blue', due: '2026-10-03' })
})
