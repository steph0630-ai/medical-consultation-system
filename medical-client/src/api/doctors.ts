import request, { unwrap } from '../utils/request'
import type { ApiResponse, Doctor } from '../types'

export const listDoctors = (departmentId: number): Promise<Doctor[]> =>
  unwrap(
    request.get<ApiResponse<Doctor[]>>('/doctors', {
      params: { department_id: departmentId },
    }),
  )
