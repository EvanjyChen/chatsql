export interface DatabaseSchema { id: number; name: string; display_name: string; description: string; exercise_count: number }
export interface Hint { level: number; text: string }
export interface Exercise { id: number; title: string; description: string; difficulty: 'easy'|'medium'|'hard'; order?: number; initial_query: string; hints: Hint[]; schema: { id:number; name:string; display_name:string; db_name:string }; tags: string[]; completed?: boolean }
export interface QueryResult { success: boolean; columns: string[]; rows: any[][]; row_count: number; execution_time: number; error?: string }
export interface SubmitResult { correct: boolean; message: string; user_result: QueryResult; diff?: any }
export interface ChatMessage { id: string; message: string; response: string; timestamp: string; isUser: boolean }
export interface AIResponse { response: string }
