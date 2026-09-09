<template>
  <main class="page">
    <header>
      <div>
        <p>预约挂号</p>
        <h1>选择科室</h1>
      </div>
      <el-button @click="$router.push('/')">返回首页</el-button>
    </header>

    <section v-loading="loading" class="department-grid">
      <button
        v-for="department in departments"
        :key="department.id"
        class="department-card"
        type="button"
        @click="selectDepartment(department)"
      >
        <strong>{{ department.name }}</strong>
        <span>{{ department.description || '暂无简介' }}</span>
      </button>
      <el-empty v-if="!loading && !departments.length" description="暂无科室" />
    </section>
  </main>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { listDepartments } from '../api/departments'
import type { Department } from '../types'

const departments = ref<Department[]>([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    departments.value = (await listDepartments()).items
  } finally {
    loading.value = false
  }
})

function selectDepartment(department: Department) {
  ElMessage.info(`已选择${department.name}，下一步将选择医生`)
}
</script>

<style scoped>
.page {
  width: min(960px, calc(100% - 40px));
  margin: 0 auto;
  padding: 48px 0;
}

header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

header p {
  margin: 0 0 6px;
  color: #409eff;
}

h1 {
  margin: 0;
}

.department-grid {
  min-height: 240px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.department-card {
  min-height: 140px;
  padding: 22px;
  text-align: left;
  color: inherit;
  border: 1px solid #e4e7ed;
  border-radius: 12px;
  background: white;
  cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.department-card:hover {
  border-color: #409eff;
  box-shadow: 0 6px 18px rgb(64 158 255 / 15%);
}

.department-card strong,
.department-card span {
  display: block;
}

.department-card strong {
  margin-bottom: 12px;
  font-size: 18px;
}

.department-card span {
  color: #909399;
  line-height: 1.7;
}

@media (max-width: 720px) {
  .department-grid {
    grid-template-columns: 1fr;
  }
}
</style>
