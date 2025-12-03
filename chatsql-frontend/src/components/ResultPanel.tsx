import React from 'react'
import type { QueryResult, SubmitResult } from '../types'

interface Props {
  queryResult: QueryResult | null
  submitResult: SubmitResult | null
}

export default function ResultPanel({ queryResult, submitResult }: Props) {
  if (!queryResult && !submitResult) {
    return (
      <div className="h-full flex flex-col items-center justify-center text-gray-300">
        <svg className="w-12 h-12 mb-3 opacity-20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 10h18M3 14h18m-9-4v8m-7 0h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
        <span className="text-xs font-bold uppercase tracking-widest opacity-50">No Results Yet</span>
      </div>
    )
  }

  return (
    <div className="h-full flex flex-col bg-white p-4">
      {/* 🟢 结果反馈卡片：Rounded-2xl */}
      {submitResult && (
        <div className="shrink-0 mb-4 animate-fade-in-up">
          <div
            className={`flex items-start gap-3 p-4 rounded-2xl border shadow-sm ${
              submitResult.correct 
                ? 'bg-green-50/50 border-green-100 text-green-900' 
                : 'bg-red-50/50 border-red-100 text-red-900'
            }`}
          >
            <div className={`mt-0.5 w-6 h-6 rounded-full flex items-center justify-center shrink-0 ${submitResult.correct ? 'bg-green-200 text-green-700' : 'bg-red-200 text-red-700'}`}>
              {submitResult.correct ? (
                <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" /></svg>
              ) : (
                <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M6 18L18 6M6 6l12 12" /></svg>
              )}
            </div>
            <div className="flex-1">
              <h4 className="text-sm font-bold mb-0.5">{submitResult.correct ? 'Correct Answer' : 'Incorrect Answer'}</h4>
              <p className="text-xs opacity-90 leading-relaxed font-medium">{submitResult.message}</p>
            </div>
          </div>
        </div>
      )}

      {queryResult && (
        <div className="flex-1 overflow-hidden flex flex-col rounded-2xl border border-gray-100 shadow-sm">
          {queryResult.error ? (
            <div className="p-6 bg-red-50/30 h-full">
               <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-red-100 text-red-700 font-bold text-[10px] uppercase mb-3 tracking-wide">
                 Error
               </div>
               <pre className="font-mono text-red-600 text-xs overflow-x-auto whitespace-pre-wrap leading-relaxed">
                 {queryResult.error}
               </pre>
            </div>
          ) : (
            <>
              {/* Stat Bar */}
              <div className="h-10 shrink-0 flex items-center justify-between px-4 bg-gray-50/50 border-b border-gray-100">
                <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">Query Result</span>
                <span className="text-[10px] font-medium text-gray-400">{queryResult.rows.length} rows</span>
              </div>
              
              {/* Table Container */}
              <div className="flex-1 overflow-auto custom-scrollbar bg-white">
                <table className="min-w-full text-left text-sm whitespace-nowrap">
                  <thead className="sticky top-0 bg-white shadow-[0_1px_2px_rgba(0,0,0,0.02)] z-10">
                    <tr>
                      {queryResult.columns.map((c, i) => (
                        <th key={i} className="px-5 py-3 text-xs font-bold text-gray-500 border-b border-gray-100/80 bg-gray-50/30 backdrop-blur-sm">
                          {c}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-50">
                    {queryResult.rows.map((r, ri) => (
                      <tr key={ri} className="hover:bg-blue-50/30 transition-colors group">
                        {r.map((c, ci) => (
                          <td key={ci} className="px-5 py-2.5 text-gray-600 font-mono text-[11px]">
                            {c === null ? <span className="text-gray-300 italic">null</span> : String(c)}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  )
}