from app.route import create_app
from app.core.config import settings


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.API_PORT,
        reload=settings.ENV == "development",
        workers=1 if settings.ENV == "development" else 4,
        env_file=".env",
    )
