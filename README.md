# 智能医疗咨询系统

基于 FastAPI 和 Vue 的医疗咨询、预约与诊疗流程系统。

## 后端启动

```powershell
cd Backend
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
docker compose up -d
.\.venv\Scripts\uvicorn app.main:app --reload --port 8001
```

健康检查：`http://localhost:8001/api/v1/config/health`

患者接口：

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/users/me`

## 患者端启动

```powershell
cd medical-client
npm install
npm run dev
```

访问：`http://localhost:3001`
