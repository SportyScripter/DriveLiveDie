import { createLazyFileRoute } from '@tanstack/react-router'

export const Route = createLazyFileRoute('/login')({
  component: Login,
})

export function Login() {
  return <div className="p-2">Hello from Login!</div>
}