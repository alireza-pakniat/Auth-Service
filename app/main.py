from fastapi import FastAPI
from app.auth import router as auth_router
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# ثبت روت احراز هویت
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

app.mount("/static", StaticFiles(directory="static"), name="static")
