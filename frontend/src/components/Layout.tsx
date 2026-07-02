import { ReactNode } from 'react'
import Header from './Header'
import Sidebar from './Sidebar'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="flex min-h-screen bg-slate-950 text-slate-100">
      <Sidebar />
      <div className="flex-1">
        <Header />
        <main className="min-h-screen overflow-auto px-6 py-8 pt-28 lg:px-10">
          <div className="mx-auto w-full max-w-[1520px]">{children}</div>
        </main>
      </div>
    </div>
  )
}
