<template>
  <main class="page">
    <header>
      <div>
        <p>预约挂号</p>
        <h1>{{ selectedDepartment ? '选择医生' : '选择科室' }}</h1>
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

    <section v-else>
      <div class="selection-bar">
        <span>已选科室：<strong>{{ selectedDepartment.name }}</strong></span>
        <el-button link type="primary" @click="selectedDepartment = null">重新选择</el-button>
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
  </main>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { listDepartments } from '../api/departments'
import { listDoctors } from '../api/doctors'
import type { Department, Doctor } from '../types'

const departments = ref<Department[]>([])
const doctors = ref<Doctor[]>([])
const selectedDepartment = ref<Department | null>(null)
const loading = ref(false)

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
  ElMessage.info(`已选择${doctor.last_name}${doctor.first_name}医生，下一步将选择时间`)
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

@media (max-width: 720px) {
  .card-grid {
    grid-template-columns: 1fr;
  }
}
</style>
