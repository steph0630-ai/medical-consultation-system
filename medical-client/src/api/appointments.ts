import request, { unwrap } from '../utils/request'
import type { ApiResponse, Appointment, AppointmentCreate, Page } from '../types'

export const createAppointment = (data: AppointmentCreate): Promise<Appointment> =>
  unwrap(request.post<ApiResponse<Appointment>>('/appointments', data))

export const listAppointments = (): Promise<Page<Appointment>> =>
  unwrap(
    request.get<ApiResponse<Page<Appointment>>>('/appointments', {
      params: { page: 1, per_page: 50 },
    }),
  )
