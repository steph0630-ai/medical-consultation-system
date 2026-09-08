# 智能医疗咨询系统

基于 FastAPI 和 Vue 的医疗咨询、预约与诊疗流程系统。

## 后端启动

```powershell
cd Backend
python -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\uvicorn app.main:app --reload --port 8001
```

健康检查：`http://localhost:8001/api/v1/config/health`
