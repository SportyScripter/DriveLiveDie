import { RouterProvider, createRouter } from '@tanstack/react-router'
import { StrictMode } from 'react'
import ReactDOM from 'react-dom/client'

import './index.css'

// Import the generated route tree
import { routeTree } from './routeTree.gen'

import { AuthProvider, useAuth } from './auth'


// Create a new router instance
const router = createRouter({ routeTree, defaultPreload: 'intent',
  context: {
    auth: undefined!, // This will be set after we wrap the app in an AuthProvider
  }, })

// Register the router instance for type safety
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}

function InnerApp() {
  const auth = useAuth()
  return <RouterProvider router={router} context={{ auth }} />
}

// Render the app
const rootElement = document.getElementById('root')!

if (!rootElement.innerHTML) {
  
  const root = ReactDOM.createRoot(rootElement)
  root.render(
    <StrictMode>
<AuthProvider>
      <InnerApp />
    </AuthProvider>    </StrictMode>,
  )
}