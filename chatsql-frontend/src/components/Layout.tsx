import React, { useState, useEffect } from 'react'
import Split from 'react-split'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

import ProblemDescription from './ProblemDescription'
import CodeEditor from './CodeEditor'
import ResultPanel from './ResultPanel'
import AIChat from './AIChat'
import type { Exercise } from '../types'
import { getExercise, getExercises } from '../services/api'

const SidebarItem = ({ ex, isActive, onClick }: { ex: Exercise; isActive: boolean; onClick: () => void }) => (
  <div
    onClick={onClick}
    className={`
      group flex items-center justify-between px-4 py-2.5 mb-1 mx-2 rounded-full cursor-pointer text-sm transition-all
      ${isActive 
        ? 'bg-white text-blue-600 shadow-sm ring-1 ring-black/5 font-semibold' 
        : 'text-gray-500 hover:bg-gray-200/50 hover:text-gray-900'
      }
    `}
  >
    <div className="flex items-center gap-3 truncate">
      <span className={`text-[10px] font-mono ${isActive ? 'text-blue-500' : 'text-gray-400'}`}>
        {String(ex.id).padStart(2, '0')}
      </span>
      <span className="truncate">{ex.title}</span>
    </div>
    {isActive && <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />}
  </div>
)

const Layout: React.FC = () => {
  const { isAuthenticated, username, setAuth } = useAuth()
  const navigate = useNavigate()

  const [exercises, setExercises] = useState<Exercise[]>([])
  const [selectedExerciseId, setSelectedExerciseId] = useState<number | null>(null)
  const [currentExercise, setCurrentExercise] = useState<Exercise | null>(null)
  const [code, setCode] = useState<string>('')
  const [queryResult, setQueryResult] = useState<any | null>(null)
  const [submitResult, setSubmitResult] = useState<any | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  
  // Layout State
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)
  const [isAIChatOpen, setIsAIChatOpen] = useState(true)
  const [demoMode, setDemoMode] = useState<boolean>(false)

  useEffect(() => {
    async function fetchList() {
      try {
        const list = await getExercises(demoMode)
        setExercises(list)
        if (list.length > 0 && !selectedExerciseId) setSelectedExerciseId(list[0].id)
      } catch (e) { console.error(e) }
    }
    fetchList()
  }, [demoMode])

  useEffect(() => {
    if (selectedExerciseId) loadExercise(selectedExerciseId)
  }, [selectedExerciseId, demoMode])

  const loadExercise = async (id: number) => {
    try {
      setIsLoading(true)
      const ex = await getExercise(id, demoMode)
      setCurrentExercise(ex)
      setCode(ex.initial_query || 'SELECT 1')
      setQueryResult(null)
      setSubmitResult(null)
    } catch (e) { console.error(e) } finally { setIsLoading(false) }
  }

  const handleLogout = () => {
    if (setAuth) setAuth({ isAuthenticated: false, username: '' })
    navigate('/auth')
  }

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch((e) => console.error(e))
    } else {
      if (document.exitFullscreen) document.exitFullscreen()
    }
  }

  return (
    <div className="h-screen w-screen bg-[#F5F5F7] p-4 flex items-center justify-center font-sans text-gray-900 overflow-hidden">
      
      {/* 🔴 App Window Container: 3 Columns (Left Sidebar | Main | Right Sidebar) */}
      <div className="w-full h-full max-w-[1920px] bg-white rounded-3xl shadow-[0_20px_50px_-12px_rgba(0,0,0,0.1)] border border-gray-200/50 overflow-hidden flex relative transition-all">
        
        {/* 1️⃣ LEFT SIDEBAR */}
        <aside 
          className={`
            flex-shrink-0 bg-[#FAFAFA] border-r border-gray-100 flex flex-col transition-all duration-300 ease-[cubic-bezier(0.25,0.1,0.25,1)] overflow-hidden
            ${isSidebarOpen ? 'w-[280px] opacity-100' : 'w-0 opacity-0 border-none'}
          `}
        >
          {/* Header */}
          <div className="h-14 flex items-center justify-between px-6 shrink-0">
            <div className="flex items-center gap-2 group">
               <button onClick={() => setIsSidebarOpen(false)} className="w-3 h-3 rounded-full bg-[#FF5F57] hover:bg-[#FF5F57]/80 border border-[#E05E58] shadow-sm transition-colors" title="Close Sidebar" />
               <button onClick={() => setIsAIChatOpen(!isAIChatOpen)} className="w-3 h-3 rounded-full bg-[#FEBC2E] hover:bg-[#FEBC2E]/80 border border-[#DFA023] shadow-sm transition-colors" title={isAIChatOpen ? "Hide AI Chat" : "Show AI Chat"} />
               <button onClick={toggleFullscreen} className="w-3 h-3 rounded-full bg-[#28C840] hover:bg-[#28C840]/80 border border-[#23AD37] shadow-sm transition-colors" title="Toggle Fullscreen" />
            </div>
            <button onClick={() => setDemoMode(!demoMode)} className={`text-[10px] font-bold px-3 py-1 rounded-full border transition-all ${demoMode ? 'bg-green-500 text-white border-transparent' : 'bg-white text-gray-400 border-gray-200'}`}>
              {demoMode ? 'DEMO' : 'MOCK'}
            </button>
          </div>

          <div className="px-6 py-2"><h2 className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4">Problem List</h2></div>
          <div className="flex-1 overflow-y-auto custom-scrollbar px-2 pb-4 space-y-0.5">
            {exercises.map(ex => (<SidebarItem key={ex.id} ex={ex} isActive={selectedExerciseId === ex.id} onClick={() => setSelectedExerciseId(ex.id)} />))}
          </div>

          <div className="p-4 bg-[#FAFAFA] border-t border-gray-100">
             {isAuthenticated ? (
               <div className="flex items-center gap-3 p-2 rounded-full bg-white border border-gray-100 shadow-sm">
                 <div className="w-9 h-9 rounded-full bg-gradient-to-br from-gray-700 to-black flex items-center justify-center text-xs font-bold text-white shrink-0">{username ? username.charAt(0).toUpperCase() : 'U'}</div>
                 <div className="flex-1 min-w-0"><div className="text-xs font-bold text-gray-800 truncate">{username || 'User'}</div><div className="text-[10px] text-gray-400">Pro Plan</div></div>
                 <button onClick={handleLogout} className="w-8 h-8 flex items-center justify-center rounded-full hover:bg-red-50 text-gray-300 hover:text-red-500 transition-colors"><svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg></button>
               </div>
             ) : (
               <button onClick={() => navigate('/auth')} className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gray-900 hover:bg-black text-white text-xs font-bold rounded-full transition-all shadow-lg shadow-gray-900/10 active:scale-[0.98]">
                 <span>Sign In</span>
                 <svg className="w-3.5 h-3.5 opacity-70" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" /></svg>
               </button>
             )}
          </div>
        </aside>

        {/* 2️⃣ MAIN CONTENT (Center) */}
        <main className="flex-1 flex flex-col min-w-0 bg-white relative z-0">
          <div className="h-14 border-b border-gray-50 flex items-center px-5 shrink-0 justify-between bg-white z-20">
            <div className="flex items-center gap-4">
               {/* Show Sidebar Toggle (visible if closed) */}
               {!isSidebarOpen && (
                 <button onClick={() => setIsSidebarOpen(true)} className="p-2 rounded-full hover:bg-gray-100 text-gray-400 transition-colors" title="Open Sidebar">
                   <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" /></svg>
                 </button>
               )}
               <div className="flex items-center gap-2 text-sm">
                  <span className="text-gray-400 font-medium">Problem</span>
                  <svg className="w-3 h-3 text-gray-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" /></svg>
                  <span className="font-bold text-gray-800 tracking-tight">{currentExercise?.title || 'Loading...'}</span>
               </div>
            </div>

            <div className="flex items-center gap-3">
                {isLoading && <span className="text-[10px] font-bold text-gray-300 animate-pulse uppercase tracking-wider">Syncing...</span>}
                {/* Show AI Chat Toggle (visible if closed) */}
                {!isAIChatOpen && (
                    <button onClick={() => setIsAIChatOpen(true)} className={`p-2 rounded-full transition-all duration-200 text-gray-400 hover:bg-gray-50 hover:text-gray-600`} title="Open AI Chat">
                      <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" /></svg>
                    </button>
                )}
            </div>
          </div>

          <div className="flex-1 relative overflow-hidden">
              <Split 
                className="split h-full flex" 
                sizes={[40, 60]} // 只有两列，分配给 Description 和 Editor
                minSize={[200, 300]} 
                gutterSize={2} 
                snapOffset={30}
              >
                <div className="h-full overflow-y-auto custom-scrollbar bg-white">
                  <ProblemDescription exercise={currentExercise} />
                </div>
                <div className="h-full flex flex-col min-w-0 bg-white border-l border-gray-50">
                  <Split direction="vertical" className="split split--vertical h-full flex flex-col" sizes={[60, 40]} minSize={[100, 100]} gutterSize={2}>
                    <div className="flex-1 min-h-0 bg-white relative">
                      <CodeEditor value={code} onChange={setCode} exercise={currentExercise} onExecute={setQueryResult} onSubmit={setSubmitResult} isLoading={isLoading} demoMode={demoMode} />
                    </div>
                    <div className="flex-1 min-h-0 bg-white border-t border-gray-100">
                      <ResultPanel queryResult={queryResult} submitResult={submitResult} />
                    </div>
                  </Split>
                </div>
              </Split>
          </div>
        </main>

        {/* 3️⃣ RIGHT SIDEBAR (AI Chat) */}
        <aside 
          className={`
            flex-shrink-0 bg-[#FAFAFA] border-l border-gray-100 flex flex-col transition-all duration-300 ease-[cubic-bezier(0.25,0.1,0.25,1)] overflow-hidden
            ${isAIChatOpen ? 'w-[320px] opacity-100' : 'w-0 opacity-0 border-none'}
          `}
        >
           {/* 传递 onClose 给 Header 显示关闭按钮 */}
           <AIChat 
             exercise={currentExercise} 
             userQuery={code} 
             error={queryResult?.error} 
             demoMode={demoMode} 
             onClose={() => setIsAIChatOpen(false)}
           />
        </aside>

      </div>
    </div>
  )
}

export default Layout