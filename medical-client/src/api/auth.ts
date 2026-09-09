import request from '../utils/request'
import type { LoginRequest, RegisterRequest, TokenResponse, User } from '../types'

export const register = (data: RegisterRequest): Promise<{ user_id: number; email: string }> =>
  request.post<unknown, { user_id: number; email: string }>('/auth/register', data)

export const login = (data: LoginRequest): Promise<TokenResponse> =>
  request.post<unknown, TokenResponse>('/auth/login', data)

export const getMyProfile = (): Promise<User> => request.get<unknown, User>('/users/me')
