export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

export interface PaginationResponse<T> {
  items: T[]
  total: number
  per_page: number
  current_page: number
  last_page: number
  has_more: boolean
}

export interface KnowledgeUploadRequest {
  source: string
  content: string
  source_type: string
}

export interface KnowledgeDocument {
  source: string
  chunk_count: number
  created_at: string
  updated_at: string
}

export interface KnowledgeCategory {
  source_type: string
  document_count: number
  chunk_count: number
  documents: KnowledgeDocument[]
}

export interface KnowledgeLibrary {
  document_count: number
  chunk_count: number
  categories: KnowledgeCategory[]
}

export interface LoginRequest {
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface Department {
  id: number
  name: string
  description?: string
  created_at: string
  updated_at: string
}

export interface DepartmentImportRequest {
  content: string
}

export interface DepartmentImportResult {
  created: string[]
  skipped: string[]
}

export interface Admin {
  id: number
  email: string
  first_name?: string
  last_name?: string
  is_active: boolean
  role?: string
  padded_id?: string
}

export interface AdminCreate {
  email: string
  password: string
  first_name?: string
  last_name?: string
  is_active?: boolean
  role?: string
}

export interface AdminUpdate {
  email?: string
  first_name?: string
  last_name?: string
  password?: string
  is_active?: boolean
}
