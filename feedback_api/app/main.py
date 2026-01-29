from fastapi import FastAPI
from app.database import Base, engine
from app.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Feedback API")

app.include_router(router)


@app.get("/")
def health_check():
    return {"status": "API is running"}
