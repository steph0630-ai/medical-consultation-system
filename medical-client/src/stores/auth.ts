import { ref } from 'vue'
import { getMyProfile } from '../api/auth'
import type { User } from '../types'
import { clearTokens, getToken } from '../utils/request'

export const currentUser = ref<User | null>(null)

export async function loadCurrentUser() {
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

export function logout() {
  currentUser.value = null
  clearTokens()
}
