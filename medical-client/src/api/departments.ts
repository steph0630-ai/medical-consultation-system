import request, { unwrap } from '../utils/request'
import type { ApiResponse, Department, Page } from '../types'

export const listDepartments = (): Promise<Page<Department>> =>
  unwrap(
    request.get<ApiResponse<Page<Department>>>('/departments', {
      params: { page: 1, per_page: 50 },
    }),
  )
