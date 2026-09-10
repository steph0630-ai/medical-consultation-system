import request, { unwrap } from '../utils/request'
import type { ApiResponse } from '../types'
import type { LoginRequest, RegisterRequest, TokenResponse, User } from '../types'

export const register = (data: RegisterRequest): Promise<{ user_id: number; email: string }> =>
  unwrap(request.post<ApiResponse<{ user_id: number; email: string }>>('/auth/register', data))

export const login = (data: LoginRequest): Promise<TokenResponse> =>
  unwrap(request.post<ApiResponse<TokenResponse>>('/auth/login', data))

export const getMyProfile = (): Promise<User> =>
  unwrap(request.get<ApiResponse<User>>('/users/me'))
