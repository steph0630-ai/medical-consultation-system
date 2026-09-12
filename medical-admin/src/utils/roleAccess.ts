export type BackofficeRole =
  | 'superadmin'
  | 'admin'
  | 'doctor'
  | 'pharmacist'
  | 'cashier'
  | 'lab'

export const roleLabels: Record<BackofficeRole, string> = {
  superadmin: '超级管理员',
  admin: '管理员',
  doctor: '医生',
  pharmacist: '药师',
  cashier: '收费员',
  lab: '检验科',
}

export function isBackofficeRole(role?: string): role is BackofficeRole {
  return Boolean(role && role in roleLabels)
}

export function getRoleHomePath(role?: string): string {
  if (role === 'superadmin') return '/departments'
  return isBackofficeRole(role) ? '/profile' : '/login'
}

export function getRoleLabel(role?: string): string {
  return isBackofficeRole(role) ? roleLabels[role] : '未知角色'
}
