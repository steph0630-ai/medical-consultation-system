# 智能医疗咨询系统

基于 FastAPI 和 Vue 的医疗咨询、预约与诊疗流程系统。

## 一键启动

```powershell
cd "D:\Users\86191\Desktop\medical-consultation-system"
docker compose up -d --build
```

该命令会同时启动后端、患者端、后台端、Celery Worker 和 Celery Beat。

患者端：`http://localhost:3001`

后台管理端：`http://localhost:3000`

接口文档：`http://localhost:8001/docs`

健康检查：`http://localhost:8001/api/v1/config/health`

API 文档导出：`http://localhost:8001/api-docs/`

- 患者端：`http://localhost:8001/api-docs/client.json`
- 后台端：`http://localhost:8001/api-docs/backoffice.json`

停止服务：

```powershell
docker compose down
```

开发环境启动：

```powershell
docker compose -f Backend/docker-compose.yml -f Backend/docker-compose.dev.yml up -d --build
```

可选监控与接口代理：

```powershell
docker compose --profile monitoring --profile proxy up -d --build
```

Flower：`http://localhost:5556`

Nginx 接口代理：`http://localhost:8086`

患者接口：

- `POST /api/v1/demo`
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/users/me`
- `POST /api/v1/triage/chat`
- `POST /api/v1/triage/chat/stream`
- `GET /api/v1/departments`
- `GET /api/v1/departments/{department_id}`
- `GET /api/v1/doctors?department_id=1`
- `GET /api/v1/doctors/{doctor_id}`
- `POST /api/v1/appointments`
- `GET /api/v1/appointments`
- `DELETE /api/v1/appointments/{appointment_id}`
- `GET /api/v1/prescriptions`
- `GET /api/v1/prescriptions/{prescription_id}`
- `PUT /api/v1/prescriptions/{prescription_id}/items/{item_id}/selection`
- `POST /api/v1/prescriptions/{prescription_id}/bill`
- `GET /api/v1/bills`
- `POST /api/v1/bills/{bill_id}/pay`
- `GET /api/v1/bills/{bill_id}/payment-status`
- `GET /api/v1/reports`
- `POST /api/v1/reports/{report_id}/chat`
- `POST /api/v1/reports/{report_id}/chat/stream`
- `GET /api/v1/medical-records`
- `GET /api/v1/aws/temporary-credentials`
- `POST /api/v1/aws/presigned-upload-url`
- `GET /api/v1/aws/presigned-download-url`

后台接口：

- `POST /api/v1/backoffice/auth/login`
- `POST /api/v1/backoffice/auth/refresh`
- `POST /api/v1/backoffice/auth/logout`
- `POST /api/v1/backoffice/admins`
- `GET /api/v1/backoffice/admins`
- `GET /api/v1/backoffice/admins/{admin_id}`
- `PUT /api/v1/backoffice/admins/{admin_id}`
- `DELETE /api/v1/backoffice/admins/{admin_id}`
- `POST /api/v1/backoffice/admins/{admin_id}/change-password`
- `POST /api/v1/backoffice/admins/{admin_id}/reset-password`
- `POST /api/v1/backoffice/departments`
- `GET /api/v1/backoffice/departments`
- `GET /api/v1/backoffice/departments/{department_id}`
- `PUT /api/v1/backoffice/departments/{department_id}`
- `DELETE /api/v1/backoffice/departments/{department_id}`
- `POST /api/v1/backoffice/departments/import-md`
- `GET /api/v1/backoffice/knowledge`
- `POST /api/v1/backoffice/knowledge`
- `POST /api/v1/backoffice/doctors`
- `GET /api/v1/backoffice/doctors`
- `GET /api/v1/backoffice/doctors/{doctor_id}`
- `PUT /api/v1/backoffice/doctors/{doctor_id}`
- `DELETE /api/v1/backoffice/doctors/{doctor_id}`
- `GET /api/v1/backoffice/drugs`
- `POST /api/v1/backoffice/drugs`
- `PUT /api/v1/backoffice/drugs/{drug_id}`
- `DELETE /api/v1/backoffice/drugs/{drug_id}`
- `GET /api/v1/backoffice/appointments`
- `PUT /api/v1/backoffice/appointments/{appointment_id}`
- `POST /api/v1/backoffice/medical-records`
- `POST /api/v1/backoffice/prescriptions`
- `GET /api/v1/backoffice/prescriptions`
- `POST /api/v1/backoffice/prescriptions/{prescription_id}/dispense`
- `GET /api/v1/backoffice/bills`
- `POST /api/v1/backoffice/bills/{bill_id}/settle`
- `GET /api/v1/backoffice/reports/exam-pending`
- `GET /api/v1/backoffice/reports`
- `POST /api/v1/backoffice/reports`
- `POST /api/v1/backoffice/reports/upload-csv`
- `POST /api/v1/backoffice/reports/{report_id}/retry-interpretation`
- `GET /api/v1/backoffice/ai-monitor/overview`
- `GET /api/v1/backoffice/aws/temporary-credentials`

首次启动后初始化原项目内置后台账号：

```powershell
docker compose exec backend python scripts/init_data.py
```

超级管理员账号：`superadmin@test.com`，密码：`admin123`

启用报告 AI 解读前，复制 `Backend/.env.example` 为 `Backend/.env`，并填写：

- `DASHSCOPE_API_KEY`
- `DEEPSEEK_API_KEY`

邮件功能按需在 `Backend/.env` 中填写 SMTP 或 Brevo 配置；未使用邮件功能时可保留示例值。

## 本地开发患者端

```powershell
cd medical-client
npm install
npm run dev
```

访问：`http://localhost:3001`

## 本地开发后台管理端

```powershell
cd medical-admin
npm install
npm run dev
```

访问：`http://localhost:3000`
