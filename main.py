from app.core.logger import logger
from app.core.factory import Application

app = Application().create_app()

if __name__ == "__main__":
    import uvicorn

    logger.info("Starting uvicorn in reload mode")
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        reload=True,
        port=int("8000"),
    )
