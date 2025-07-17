from fastapi import FastAPI
from app.auth import router as auth_router
from fastapi.staticfiles import StaticFiles
from app.database import init_db


app = FastAPI()
init_db()  # ← Add this


# ثبت روت احراز هویت
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

app.mount("/static", StaticFiles(directory="static"), name="static")
