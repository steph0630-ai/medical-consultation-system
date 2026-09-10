export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest extends LoginRequest {
  first_name: string
  last_name: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface User {
  id: number
  email: string
  first_name: string
  last_name: string
}

export interface ApiResponse<T> {
  code: number
  message: string
  data: T
}

export interface Department {
  id: number
  name: string
  description: string | null
  created_at: string
}

export interface Page<T> {
  items: T[]
  total: number
  page: number
  per_page: number
}

export interface Doctor {
  id: number
  department_id: number
  department_name: string
  first_name: string
  last_name: string
  title: string | null
  introduction: string | null
  created_at: string
}

export type AppointmentStatus = 'pending' | 'confirmed' | 'waiting_exam' | 'completed' | 'cancelled'

export interface Appointment {
  id: number
  patient_id: number
  doctor_id: number
  department_id: number
  doctor_name: string
  department_name: string
  appointment_time: string
  status: AppointmentStatus
  created_at: string
}

export interface AppointmentCreate {
  doctor_id: number
  department_id: number
  appointment_time: string
}
