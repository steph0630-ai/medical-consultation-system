import request from '../utils/request'
import type { Doctor } from '../types'

export const listDoctors = (departmentId: number): Promise<Doctor[]> =>
  request.get<unknown, Doctor[]>('/doctors', {
    params: { department_id: departmentId },
  })
