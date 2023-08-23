import React from 'react'

import './App.css'

import {
  createBrowserRouter,
  RouterProvider
} from 'react-router-dom'
import './index.css'

import Home from './components/Home'

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />
  }
])

function App () {
  return (
    <RouterProvider router={router} />
  )
}

export default App
