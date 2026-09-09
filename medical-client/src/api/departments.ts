import request from '../utils/request'
import type { Department, Page } from '../types'

export const listDepartments = (): Promise<Page<Department>> =>
  request.get<unknown, Page<Department>>('/departments', {
    params: { page: 1, per_page: 50 },
  })
