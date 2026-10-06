import { screen } from '@testing-library/react'
import { expect, test, vi } from 'vitest'
import { renderWithProviders } from '../../test/render'
import { CheckPanel } from './CheckPanel'

test('requires a URL or text and does not call onCheck', async () => {
  const onCheck = vi.fn()
  const { user } = renderWithProviders(<CheckPanel onCheck={onCheck} />)
  await user.click(screen.getByRole('button', { name: 'Check' }))
  expect(await screen.findByText('Enter a release URL or paste release text')).toBeTruthy()
  expect(onCheck).not.toHaveBeenCalled()
})

test('rejects a non-http URL', async () => {
  const onCheck = vi.fn()
  const { user } = renderWithProviders(<CheckPanel onCheck={onCheck} />)
  await user.type(screen.getByLabelText('Release URL'), 'not a url')
  await user.click(screen.getByRole('button', { name: 'Check' }))
  expect(await screen.findByText('Enter a valid http(s) URL')).toBeTruthy()
  expect(onCheck).not.toHaveBeenCalled()
})

test('submits only the filled fields', async () => {
  const onCheck = vi.fn().mockResolvedValue(undefined)
  const { user } = renderWithProviders(<CheckPanel onCheck={onCheck} />)
  await user.type(screen.getByLabelText('Release URL'), 'https://example.com/release')
  await user.click(screen.getByRole('button', { name: 'Check' }))
  await vi.waitFor(() => expect(onCheck).toHaveBeenCalledWith({ release_url: 'https://example.com/release' }))
})

test('submits pasted text alone', async () => {
  const onCheck = vi.fn().mockResolvedValue(undefined)
  const { user } = renderWithProviders(<CheckPanel onCheck={onCheck} />)
  await user.type(screen.getByLabelText('Or paste release text'), 'v2 drops X')
  await user.click(screen.getByRole('button', { name: 'Check' }))
  await vi.waitFor(() => expect(onCheck).toHaveBeenCalledWith({ release_text: 'v2 drops X' }))
})

test('pending disables the button and shows a spinner; error shows an alert', () => {
  renderWithProviders(<CheckPanel onCheck={vi.fn()} pending error="Check failed" />)
  expect((screen.getByRole('button', { name: /Check/ }) as HTMLButtonElement).disabled).toBe(true)
  expect(screen.getByRole('progressbar')).toBeTruthy()
  expect(screen.getByRole('alert').textContent).toContain('Check failed')
})
