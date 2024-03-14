import { createLazyFileRoute } from '@tanstack/react-router'

export const Route = createLazyFileRoute('/dashboard')({
  component: Dashboard,
})

export function Dashboard() {
  return <div className="p-2">Hello from Dashboard!</div>
}