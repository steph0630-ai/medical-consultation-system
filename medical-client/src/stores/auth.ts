import { ref } from 'vue'
import { getMyProfile } from '../api/user'
import type { User } from '../types/api'
import { clearToken, getToken } from '../utils/request'

export const currentUser = ref<User | null>(null)

export async function loadCurrentUser(): Promise<User | null> {
  if (!getToken()) {
    currentUser.value = null
    return null
  }
  try {
    currentUser.value = await getMyProfile()
    return currentUser.value
  } catch {
    currentUser.value = null
    return null
  }
}

export function clearCurrentUser(): void {
  currentUser.value = null
  clearToken()
}
