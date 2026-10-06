import { cleanup, configure } from '@testing-library/react'
import { afterEach } from 'vitest'

// Lazy route chunks transform on first use; the 1 s default flakes when test files run in parallel.
configure({ asyncUtilTimeout: 5000 })

afterEach(() => {
  cleanup()
  localStorage.clear()
})

// jsdom lacks matchMedia, which MUI's colour-scheme manager needs.
if (!window.matchMedia) {
  window.matchMedia = (query: string) =>
    ({
      matches: false,
      media: query,
      onchange: null,
      addListener: () => {},
      removeListener: () => {},
      addEventListener: () => {},
      removeEventListener: () => {},
      dispatchEvent: () => false,
    }) as MediaQueryList
}
