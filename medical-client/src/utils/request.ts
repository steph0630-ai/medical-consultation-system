import axios from 'axios'
import { ElMessage } from 'element-plus'
import type { ApiResponse } from '../types'

const ACCESS_TOKEN_KEY = 'client_access_token'
const REFRESH_TOKEN_KEY = 'client_refresh_token'

export const getToken = () => localStorage.getItem(ACCESS_TOKEN_KEY)

export function setTokens(accessToken: string, refreshToken: string) {
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken)
  localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken)
}

export function clearTokens() {
  localStorage.removeItem(ACCESS_TOKEN_KEY)
  localStorage.removeItem(REFRESH_TOKEN_KEY)
}

const request = axios.create({ baseURL: '/api/v1', timeout: 15_000 })

request.interceptors.request.use((config) => {
  const token = getToken()
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

request.interceptors.response.use(
  (response) => (response.data as ApiResponse<unknown>).data,
  (error) => {
    const status = error.response?.status
    const message = error.response?.data?.message ?? error.response?.data?.detail ?? '请求失败'
    ElMessage.error(message)
    if (status === 401 || status === 403) clearTokens()
    return Promise.reject(error)
  },
)

export default request
