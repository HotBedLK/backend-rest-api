import os

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import get_supabase_client

load_dotenv()
from services.AuthService.app.main import app as auth_service_app
from services.AdminService.app.main import app as admin_service_app
from services.AutomationService.app.main import app as automation_service_app
from services.NotificationService.app.main import app as notification_service_app
from services.GeneralUserService.app.main import app as general_user_service_app
from services.CashingService.app.main import app as cashing_service_app

app = FastAPI(title="Main API")

#cores add kara
cors_origins = [origin.strip() for origin in os.getenv("CORS_ALLOW_ORIGINS", "*").split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/auth", auth_service_app)
app.mount("/admin", admin_service_app)
app.mount("/notification",notification_service_app)
app.mount("/general",general_user_service_app)


@app.get("/health")
def health_check():
    return {"status": "ok"}


