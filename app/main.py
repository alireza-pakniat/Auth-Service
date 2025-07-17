from fastapi import FastAPI
from app.auth import router as auth_router
from fastapi.staticfiles import StaticFiles
from app.database import init_db
from fastapi.responses import RedirectResponse
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI()
init_db()  


app.include_router(auth_router, prefix="/auth", tags=["Auth"])

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return RedirectResponse(url="/static/auth.html")

Instrumentator().instrument(app).expose(app)
