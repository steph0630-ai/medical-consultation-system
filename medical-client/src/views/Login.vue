<template>
  <main class="login-page">
    <section class="login-card">
      <header>
        <h1>智慧医院</h1>
        <p>患者服务平台</p>
      </header>

      <el-tabs v-model="activeTab" stretch>
        <el-tab-pane label="登录" name="login">
          <el-form label-position="top" @submit.prevent="handleLogin">
            <el-form-item label="邮箱">
              <el-input v-model="loginForm.email" placeholder="请输入邮箱" />
            </el-form-item>
            <el-form-item label="密码">
              <el-input v-model="loginForm.password" type="password" show-password placeholder="请输入密码" />
            </el-form-item>
            <el-button native-type="submit" type="primary" :loading="submitting">登录</el-button>
          </el-form>
        </el-tab-pane>

        <el-tab-pane label="注册" name="register">
          <el-form label-position="top" @submit.prevent="handleRegister">
            <el-form-item label="邮箱">
              <el-input v-model="registerForm.email" placeholder="请输入邮箱" />
            </el-form-item>
            <div class="name-row">
              <el-form-item label="姓">
                <el-input v-model="registerForm.last_name" />
              </el-form-item>
              <el-form-item label="名">
                <el-input v-model="registerForm.first_name" />
              </el-form-item>
            </div>
            <el-form-item label="密码">
              <el-input v-model="registerForm.password" type="password" show-password placeholder="至少8位，含字母和数字" />
            </el-form-item>
            <el-button native-type="submit" type="primary" :loading="submitting">注册</el-button>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </section>
  </main>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { login, register } from '../api/auth'
import { loadCurrentUser } from '../stores/auth'
import { setTokens } from '../utils/request'

const router = useRouter()
const activeTab = ref('login')
const submitting = ref(false)
const loginForm = reactive({ email: '', password: '' })
const registerForm = reactive({ email: '', password: '', first_name: '', last_name: '' })

async function handleLogin() {
  if (!loginForm.email.trim() || !loginForm.password) return ElMessage.warning('请填写邮箱和密码')
  submitting.value = true
  try {
    const tokens = await login({ email: loginForm.email.trim(), password: loginForm.password })
    setTokens(tokens.access_token, tokens.refresh_token)
    if (!(await loadCurrentUser())) return
    ElMessage.success('登录成功')
    await router.push('/')
  } finally {
    submitting.value = false
  }
}

async function handleRegister() {
  const data = {
    email: registerForm.email.trim(),
    password: registerForm.password,
    first_name: registerForm.first_name.trim(),
    last_name: registerForm.last_name.trim(),
  }
  if (Object.values(data).some((value) => !value)) return ElMessage.warning('请填写完整信息')
  if (data.password.length < 8 || !/[A-Za-z]/.test(data.password) || !/\d/.test(data.password)) {
    return ElMessage.warning('密码至少8位，且必须包含字母和数字')
  }
  submitting.value = true
  try {
    await register(data)
    loginForm.email = data.email
    registerForm.password = ''
    activeTab.value = 'login'
    ElMessage.success('注册成功，请登录')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 24px;
  background: linear-gradient(135deg, #e3f2fd, #f8fbff);
}

.login-card {
  width: min(420px, 100%);
  padding: 32px 40px 40px;
  border-radius: 12px;
  background: white;
  box-shadow: 0 8px 32px rgb(0 0 0 / 8%);
}

header {
  margin-bottom: 16px;
  text-align: center;
}

h1 {
  margin: 0;
  color: #1976d2;
}

p {
  margin: 6px 0 0;
  color: #909399;
}

.name-row {
  display: flex;
  gap: 12px;
}

.name-row > * {
  flex: 1;
}

button {
  width: 100%;
}
</style>
