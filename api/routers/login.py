from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas.login as login_schema

import api.cruds.login as login_crud
from api.db import get_db

router = APIRouter()

# 1. 회원 조회
@router.post("/idcheck", response_model=login_schema.IdCheckResponse)
async def idcheck(idcheck_body: login_schema.IdCheck, db: AsyncSession = Depends(get_db)):
    return await login_crud.id_check(db, idcheck_body)

# 2. 로그인
@router.post("/login", response_model=login_schema.LoginResponse)
async def login(login_body: login_schema.Login, db: AsyncSession = Depends(get_db)):
    return await login_crud.login(db, login_body)