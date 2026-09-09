<template>
  <main class="home">
    <section>
      <h1>欢迎，{{ currentUser?.last_name }}{{ currentUser?.first_name }}</h1>
      <p>{{ currentUser?.email }}</p>
      <div class="actions">
        <el-button type="primary" @click="router.push('/departments')">预约挂号</el-button>
        <el-button @click="handleLogout">退出登录</el-button>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { currentUser, logout } from '../stores/auth'

const router = useRouter()

function handleLogout() {
  logout()
  router.push('/login')
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  display: grid;
  place-items: center;
}

section {
  padding: 40px;
  text-align: center;
  border-radius: 12px;
  background: white;
  box-shadow: 0 8px 32px rgb(0 0 0 / 8%);
}

.actions {
  margin-top: 24px;
}
</style>
