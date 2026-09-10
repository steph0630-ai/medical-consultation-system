<template>
  <main class="page">
    <header>
      <div>
        <p>预约挂号</p>
        <h1>{{ selectedDoctor ? '选择就诊时间' : selectedDepartment ? '选择医生' : '选择科室' }}</h1>
      </div>
      <el-button @click="$router.push('/')">返回首页</el-button>
    </header>

    <section v-if="!selectedDepartment" v-loading="loading" class="card-grid">
      <button
        v-for="department in departments"
        :key="department.id"
        class="card"
        type="button"
        @click="selectDepartment(department)"
      >
        <strong>{{ department.name }}</strong>
        <span>{{ department.description || '暂无简介' }}</span>
      </button>
      <el-empty v-if="!loading && !departments.length" description="暂无科室" />
    </section>

    <section v-else-if="!selectedDoctor">
      <div class="selection-bar">
        <span>已选科室：<strong>{{ selectedDepartment.name }}</strong></span>
        <el-button link type="primary" @click="resetDepartment">重新选择</el-button>
      </div>
      <div v-loading="loading" class="doctor-list">
        <div
          v-for="doctor in doctors"
          :key="doctor.id"
          class="doctor-card"
        >
          <span class="avatar">{{ doctor.last_name }}</span>
          <span class="doctor-info">
            <strong>{{ doctor.last_name }}{{ doctor.first_name }}</strong>
            <small>{{ doctor.title }}</small>
            <span>{{ doctor.introduction || '暂无简介' }}</span>
          </span>
          <el-button type="primary" @click="selectDoctor(doctor)">选择</el-button>
        </div>
        <el-empty v-if="!loading && !doctors.length" description="该科室暂无医生" />
      </div>
    </section>

    <section v-else class="confirm-card">
      <dl>
        <div><dt>科室</dt><dd>{{ selectedDepartment.name }}</dd></div>
        <div><dt>医生</dt><dd>{{ selectedDoctor.last_name }}{{ selectedDoctor.first_name }} · {{ selectedDoctor.title }}</dd></div>
      </dl>
      <label for="appointment-time">就诊时间</label>
      <input
        id="appointment-time"
        v-model="appointmentTime"
        type="datetime-local"
        :min="minimumTime"
      />
      <div class="confirm-actions">
        <el-button @click="selectedDoctor = null">上一步</el-button>
        <el-button type="primary" :loading="submitting" @click="submitAppointment">提交预约</el-button>
      </div>
    </section>
  </main>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { createAppointment } from '../api/appointments'
import { listDepartments } from '../api/departments'
import { listDoctors } from '../api/doctors'
import type { Department, Doctor } from '../types'

const departments = ref<Department[]>([])
const doctors = ref<Doctor[]>([])
const selectedDepartment = ref<Department | null>(null)
const selectedDoctor = ref<Doctor | null>(null)
const loading = ref(false)
const submitting = ref(false)
const appointmentTime = ref('')
const minimumTime = new Date(Date.now() - new Date().getTimezoneOffset() * 60_000)
  .toISOString()
  .slice(0, 16)
const router = useRouter()

onMounted(async () => {
  loading.value = true
  try {
    departments.value = (await listDepartments()).items
  } finally {
    loading.value = false
  }
})

async function selectDepartment(department: Department) {
  selectedDepartment.value = department
  loading.value = true
  try {
    doctors.value = await listDoctors(department.id)
  } finally {
    loading.value = false
  }
}

function selectDoctor(doctor: Doctor) {
  selectedDoctor.value = doctor
}

function resetDepartment() {
  selectedDepartment.value = null
  selectedDoctor.value = null
  doctors.value = []
}

async function submitAppointment() {
  if (!selectedDepartment.value || !selectedDoctor.value || !appointmentTime.value) {
    return ElMessage.warning('请选择就诊时间')
  }
  const time = new Date(appointmentTime.value)
  if (time <= new Date()) return ElMessage.warning('请选择未来时间')

  submitting.value = true
  try {
    await createAppointment({
      department_id: selectedDepartment.value.id,
      doctor_id: selectedDoctor.value.id,
      appointment_time: time.toISOString(),
    })
    ElMessage.success('预约成功')
    await router.push('/appointments')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.page {
  width: min(960px, calc(100% - 40px));
  margin: 0 auto;
  padding: 48px 0;
}

header,
.selection-bar,
.doctor-card {
  display: flex;
  align-items: center;
}

header,
.selection-bar {
  justify-content: space-between;
}

header {
  margin-bottom: 24px;
}

header p {
  margin: 0 0 6px;
  color: #409eff;
}

h1 {
  margin: 0;
}

.card-grid {
  min-height: 240px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.card,
.doctor-card {
  color: inherit;
  text-align: left;
  border: 1px solid #e4e7ed;
  border-radius: 12px;
  background: white;
  cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.card {
  min-height: 140px;
  padding: 22px;
}

.card:hover,
.doctor-card:hover {
  border-color: #409eff;
  box-shadow: 0 6px 18px rgb(64 158 255 / 15%);
}

.card strong,
.card span,
.doctor-info > * {
  display: block;
}

.card strong {
  margin-bottom: 12px;
  font-size: 18px;
}

.card span,
.doctor-info span {
  color: #909399;
  line-height: 1.7;
}

.selection-bar {
  margin-bottom: 16px;
  padding: 14px 18px;
  border-radius: 10px;
  background: white;
}

.doctor-list {
  min-height: 220px;
  display: grid;
  gap: 12px;
}

.doctor-card {
  width: 100%;
  padding: 16px;
  gap: 16px;
}

.avatar {
  width: 48px;
  height: 48px;
  display: grid;
  flex: 0 0 auto;
  place-items: center;
  color: white;
  border-radius: 50%;
  background: #409eff;
  font-size: 18px;
}

.doctor-info {
  flex: 1;
}

.doctor-info strong {
  font-size: 16px;
}

.doctor-info small {
  margin: 4px 0;
  color: #409eff;
}

.confirm-card {
  max-width: 620px;
  margin: 0 auto;
  padding: 28px;
  border-radius: 12px;
  background: white;
}

dl {
  margin: 0 0 24px;
}

dl div {
  display: grid;
  grid-template-columns: 100px 1fr;
  padding: 12px 0;
  border-bottom: 1px solid #ebeef5;
}

dt {
  color: #909399;
}

dd {
  margin: 0;
}

label,
input {
  display: block;
}

label {
  margin-bottom: 8px;
}

input {
  width: 100%;
  padding: 10px 12px;
  color: #303133;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  font: inherit;
}

.confirm-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 24px;
}

@media (max-width: 720px) {
  .card-grid {
    grid-template-columns: 1fr;
  }
}
</style>
