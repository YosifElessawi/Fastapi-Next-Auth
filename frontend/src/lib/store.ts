'use client';

import { configureStore } from '@reduxjs/toolkit'
import { setupListeners } from '@reduxjs/toolkit/query'
import  todoReducer  from '@/features/todo/todo-slice'

const store = configureStore({
  reducer: {
    todos: todoReducer
  },
})

setupListeners(store.dispatch)

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch

export { store };
