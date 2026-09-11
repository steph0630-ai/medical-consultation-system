import axios, { type AxiosInstance, type InternalAxiosRequestConfig } from 'axios'
import { ElMessage } from 'element-plus'
import type { ApiResponse } from '../types/api'

const TOKEN_KEY = 'client_access_token'
const REFRESH_TOKEN_KEY = 'client_refresh_token'

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token)
}

export function getRefreshToken(): string | null {
  return localStorage.getItem(REFRESH_TOKEN_KEY)
}

export function setRefreshToken(token: string): void {
  localStorage.setItem(REFRESH_TOKEN_KEY, token)
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY)
  localStorage.removeItem(REFRESH_TOKEN_KEY)
}

const request: AxiosInstance = axios.create({
  baseURL: '/api/v1',
  timeout: 60000,
})

request.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

const AUTH_FAILURE_MESSAGES = [
  'Invalid authentication credentials',
  'Inactive user',
  'Not authenticated',
]

function isAuthFailure(status?: number, message?: string): boolean {
  if (status === 401) return true
  if (status !== 403) return false
  return AUTH_FAILURE_MESSAGES.some((item) => message?.includes(item))
}

request.interceptors.response.use(
  (response) => (response.data as ApiResponse).data,
  (error) => {
    const message = error?.response?.data?.message || error.message || '请求失败'
    ElMessage.error(message)
    if (isAuthFailure(error?.response?.status, error?.response?.data?.message)) {
      clearToken()
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  },
)

export default request
