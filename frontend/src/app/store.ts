import { combineSlices, configureStore } from '@reduxjs/toolkit'
import { setupListeners } from '@reduxjs/toolkit/query'
import { notesFilterSlice } from '../features/notes/notesFilterSlice'
import { baseApi } from '../services/baseApi'

// Server data lives in baseApi (RTK Query). Add a slice here only for client state shared across components.
const rootReducer = combineSlices(baseApi, notesFilterSlice)

export type RootState = ReturnType<typeof rootReducer>

export function makeStore(preloadedState?: Partial<RootState>) {
  const store = configureStore({
    reducer: rootReducer,
    preloadedState,
    middleware: (getDefault) => getDefault().concat(baseApi.middleware),
  })
  setupListeners(store.dispatch)
  return store
}

export type AppStore = ReturnType<typeof makeStore>
export type AppDispatch = AppStore['dispatch']
