import React from 'react'

import './App.css'

import {
  createBrowserRouter,
  RouterProvider
} from 'react-router-dom'
import './index.css'

import Home from './components/Home'
import Script from './components/script/Script'

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />
  },
  {
    path: '/scripts/:id',
    element: <Script />
  }
])

function App () {
  return (
    <RouterProvider router={router} />
  )
}

export default App
