# 智能医疗咨询系统

基于 FastAPI 和 Vue 的医疗咨询、预约与诊疗流程系统。

## 一键启动

```powershell
cd Backend
docker compose up -d --build
```

患者端：`http://localhost:3001`

后台管理端：`http://localhost:3000`

接口文档：`http://localhost:8001/docs`

健康检查：`http://localhost:8001/api/v1/config/health`

停止服务：

```powershell
docker compose down
```

患者接口：

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/users/me`
- `GET /api/v1/departments`
- `GET /api/v1/departments/{department_id}`
- `GET /api/v1/doctors?department_id=1`
- `GET /api/v1/doctors/{doctor_id}`
- `POST /api/v1/appointments`
- `GET /api/v1/appointments`
- `DELETE /api/v1/appointments/{appointment_id}`

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

首次启动后初始化原项目内置后台账号：

```powershell
docker compose exec backend python scripts/init_data.py
```

超级管理员账号：`superadmin@test.com`，密码：`admin123`

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
