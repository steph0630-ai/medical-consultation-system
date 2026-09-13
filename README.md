# 智能医疗咨询系统

一个基于 FastAPI、Vue 和 PostgreSQL 的医疗咨询系统，包含智能分诊、预约挂号、医生接诊、处方、收费、发药和检验报告等功能。

## 快速启动

请先安装并启动 Docker Desktop，然后在 PowerShell 中运行：

```powershell
cd "D:\Users\86191\Desktop\medical-consultation-system"
docker compose up -d --build
```

首次启动完成后，初始化后台账号：

```powershell
docker compose exec backend python scripts/init_data.py
```

后台账号：

- 邮箱：`superadmin@test.com`
- 密码：`admin123`

## 访问地址

- 患者端：http://localhost:3001
- 后台管理端：http://localhost:3000
- 接口文档：http://localhost:8001/docs
- 健康检查：http://localhost:8001/api/v1/config/health

## AI 配置

普通功能无需配置密钥即可启动。使用智能分诊和报告解读前，请在项目根目录创建 `.env`：

```env
SECRET_KEY=请修改为随机字符串
DASHSCOPE_API_KEY=你的密钥
DEEPSEEK_API_KEY=你的密钥
```

修改后重新启动：

```powershell
docker compose up -d --build
```

## 常用命令

查看运行状态：

```powershell
docker compose ps
```

查看日志：

```powershell
docker compose logs -f
```

停止项目：

```powershell
docker compose down
```

导入药品数据：

```powershell
docker compose exec backend python scripts/seed_drugs.py
```

启动任务监控和接口代理：

```powershell
docker compose --profile monitoring --profile proxy up -d --build
```

- Flower：http://localhost:5556
- Nginx 代理：http://localhost:8086

## 单独启动前端

患者端：

```powershell
cd "D:\Users\86191\Desktop\medical-consultation-system\medical-client"
npm install
npm run dev
```

后台管理端：

```powershell
cd "D:\Users\86191\Desktop\medical-consultation-system\medical-admin"
npm install
npm run dev
```

## 技术栈

- 后端：FastAPI、SQLAlchemy、Celery
- 前端：Vue 3、TypeScript、Element Plus
- 数据库：PostgreSQL + pgvector
- 缓存与任务队列：Redis
- 部署：Docker Compose

## License

[MIT](LICENSE)
