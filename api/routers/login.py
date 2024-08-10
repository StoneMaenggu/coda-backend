from fastapi import APIRouter
import api.schemas.login as login_schema
router = APIRouter()

# 1. 회원 조회
@router.post("/idcheck", response_model=login_schema.IdCheckResponse)
async def idcheck(idcheck_body: login_schema.IdCheck):
    return login_schema.IdCheckResponse(id_exist=False, **idcheck_body.dict())

# 2. 로그인
@router.post("/login", response_model=login_schema.LoginResponse)
async def login(login_body: login_schema.Login):
    return login_schema.LoginResponse(login_success=False, **login_body.dict())