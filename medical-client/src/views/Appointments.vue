<template>
  <main class="page">
    <header>
      <h1>我的预约</h1>
      <div>
        <el-button @click="router.push('/')">返回首页</el-button>
        <el-button type="primary" @click="router.push('/departments')">新增预约</el-button>
      </div>
    </header>

    <section v-loading="loading" class="appointment-list">
      <article v-for="appointment in appointments" :key="appointment.id">
        <div>
          <strong>{{ appointment.department_name }}</strong>
          <el-tag type="warning" size="small">{{ statusLabel[appointment.status] }}</el-tag>
        </div>
        <p>医生：{{ appointment.doctor_name }}</p>
        <p>就诊时间：{{ new Date(appointment.appointment_time).toLocaleString() }}</p>
      </article>
      <el-empty v-if="!loading && !appointments.length" description="还没有预约记录" />
    </section>
  </main>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { listAppointments } from '../api/appointments'
import type { Appointment, AppointmentStatus } from '../types'

const router = useRouter()
const appointments = ref<Appointment[]>([])
const loading = ref(false)
const statusLabel: Record<AppointmentStatus, string> = {
  pending: '待确认',
  confirmed: '已确认',
  waiting_exam: '等待检查结果',
  completed: '已完成',
  cancelled: '已取消',
}

onMounted(async () => {
  loading.value = true
  try {
    appointments.value = (await listAppointments()).items
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.page {
  width: min(860px, calc(100% - 40px));
  margin: 0 auto;
  padding: 48px 0;
}

header,
article > div {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

header {
  margin-bottom: 24px;
}

h1 {
  margin: 0;
}

.appointment-list {
  min-height: 240px;
  display: grid;
  gap: 12px;
}

article {
  padding: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 12px;
  background: white;
}

article strong {
  font-size: 18px;
}

article p {
  margin: 10px 0 0;
  color: #606266;
}
</style>
