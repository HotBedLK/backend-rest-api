from fastapi import APIRouter,Depends
from supabase import Client
from typing import Annotated
from app.database.supabase import get_supabase_client
from ..schemas.loginInputSchema import LoginInputSchema


router_login  = APIRouter(tags=["Login Routes"])

@router_login.get('/send_email',description="send email to verify email address")
async def send_email():
    pass