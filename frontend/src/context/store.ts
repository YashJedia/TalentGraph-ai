import { create } from 'zustand'

interface AppState {
  darkMode: boolean
  toggleDarkMode: () => void
  selectedJobId: string | null
  setSelectedJobId: (jobId: string) => void
}

export const useAppStore = create<AppState>((set) => ({
  darkMode: true,
  toggleDarkMode: () => set((state) => ({ darkMode: !state.darkMode })),
  selectedJobId: null,
  setSelectedJobId: (jobId: string) => set({ selectedJobId: jobId }),
}))
