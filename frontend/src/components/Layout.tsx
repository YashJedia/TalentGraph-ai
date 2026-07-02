import { ReactNode, useEffect } from 'react'
import Header from './Header'
import Sidebar from './Sidebar'
import Footer from './Footer'
import { useAppStore } from '../context/store'

interface LayoutProps {
  children: ReactNode
}

export default function Layout({ children }: LayoutProps) {
  const { darkMode } = useAppStore()

  useEffect(() => {
    if (darkMode) {
      document.body.classList.remove('light-mode')
    } else {
      document.body.classList.add('light-mode')
    }
  }, [darkMode])

  return (
    <div className={`relative flex min-h-screen text-slate-100 overflow-hidden transition-colors duration-300 ${
      darkMode ? 'bg-[#0f1222]' : 'bg-[#f8fafc]'
    }`}>
      {/* Dynamic Background Blobs */}
      {darkMode && (
        <>
          <div className="blob-sky" />
          <div className="blob-violet" />
          <div className="blob-extra" />
        </>
      )}

      <div className="relative z-10 flex w-full">
        <Sidebar />
        <div className="flex-1 min-h-screen flex flex-col pl-72">
          <Header />
          <main className="flex-grow overflow-auto px-6 py-8 pt-10 lg:px-10">
            <div className="mx-auto w-full max-w-[1520px]">{children}</div>
          </main>
          <Footer />
        </div>
      </div>
    </div>
  )
}
