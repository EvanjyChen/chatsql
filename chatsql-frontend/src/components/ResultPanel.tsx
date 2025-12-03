import React from 'react'
import type { QueryResult, SubmitResult } from '../types'

interface Props {
  queryResult: QueryResult | null
  submitResult: SubmitResult | null
}

export default function ResultPanel({ queryResult, submitResult }: Props) {
  if (!queryResult && !submitResult)
    return <div className="p-6 text-gray-500">Run your query to see results</div>

  return (
    <div className="p-4">
      {submitResult && (
        <div
          className={`p-3 mb-3 rounded-xl ${submitResult.correct ? 'bg-green-100' : 'bg-red-100'}`}
        >
          <div className="font-medium text-gray-900">{submitResult.message}</div>
        </div>
      )}

      {queryResult && (
        <div>
          {queryResult.error ? (
            <pre className="text-red-600">{queryResult.error}</pre>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full table-auto text-sm">
                <thead>
                  <tr>
                    {queryResult.columns.map((c, i) => (
                      <th key={i} className="px-2 py-1 text-left">
                        {c}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {queryResult.rows.map((r, ri) => (
                    <tr key={ri}>
                      {r.map((c, ci) => (
                        <td key={ci} className="px-2 py-1">
                          {String(c)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
