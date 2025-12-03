import React, { useState, useEffect } from 'react'
import Split from 'react-split'
import ProblemModal from './ProblemModal'
import ProblemDescription from './ProblemDescription'
import CodeEditor from './CodeEditor'
import ResultPanel from './ResultPanel'
import AIChat from './AIChat'
import Header from './Header'
import type { Exercise } from '../types'
import { getExercise } from '../services/api'

const Layout: React.FC = () => {
  const [selectedExerciseId, setSelectedExerciseId] = useState<number | null>(1)
  const [demoMode, setDemoMode] = useState<boolean>(false)
  const [showProblemModal, setShowProblemModal] = useState<boolean>(false)
  const [currentExercise, setCurrentExercise] = useState<Exercise | null>(null)
  const [code, setCode] = useState<string>('')
  const [queryResult, setQueryResult] = useState<any | null>(null)
  const [submitResult, setSubmitResult] = useState<any | null>(null)
  const [isLoading, setIsLoading] = useState(false)

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
    } catch (e) {
      console.error(e)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      <Header
        demoOn={demoMode}
        onToggleDemo={() => setDemoMode((d) => !d)}
        onOpenExercises={() => setShowProblemModal(true)}
      />

      {/* Main area with padding and gap */}
      <div className="flex-1 min-h-0 pt-16">
        <div className="h-full p-2">
          <Split
            className="split h-full"
            sizes={[33, 34, 33]}
            minSize={[200, 300, 200]}
            gutterSize={1}
          >
            {/* Left: Problem Description */}
            <div className="h-full pr-1">
              <ProblemDescription exercise={currentExercise} />
            </div>

            {/* Middle: Code Editor + Results */}
            <div className="h-full px-1">
              <Split
                direction="vertical"
                className="split split--vertical h-full"
                sizes={[65, 35]}
                minSize={[300, 200]}
                gutterSize={1}
              >
                <div className="pb-1">
                  <CodeEditor
                    value={code}
                    onChange={setCode}
                    exercise={currentExercise}
                    onExecute={setQueryResult}
                    onSubmit={setSubmitResult}
                    isLoading={isLoading}
                    demoMode={demoMode}
                  />
                </div>

                <div className="pt-1 h-full">
                  <div className="h-full bg-white rounded-xl overflow-hidden">
                    <ResultPanel queryResult={queryResult} submitResult={submitResult} />
                  </div>
                </div>
              </Split>
            </div>

            {/* Right: AI Chat */}
            <div className="h-full pl-1">
              <AIChat
                exercise={currentExercise}
                userQuery={code}
                error={queryResult?.error}
                demoMode={demoMode}
              />
            </div>
          </Split>
        </div>
      </div>

      {/* Problem Modal */}
      <ProblemModal
        isOpen={showProblemModal}
        onClose={() => setShowProblemModal(false)}
        selectedId={selectedExerciseId}
        onSelect={setSelectedExerciseId}
        demoMode={demoMode}
      />
    </div>
  )
}

export default Layout
