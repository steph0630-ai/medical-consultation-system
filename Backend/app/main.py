from fastapi import FastAPI

app = FastAPI(title="智能医疗咨询系统")


@app.get("/api/v1/config/health")
async def health() -> dict:
    return {
        "code": 200,
        "message": "success",
        "data": {"status": "healthy", "services": {"api": "up"}},
    }
