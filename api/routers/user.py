from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import api.schemas.user as user_schema

import api.cruds.user as user_crud
from api.db import get_db

router = APIRouter()


# 3. 회원 가입
@router.post("/register", response_model=user_schema.RegisterResponse)
async def register(register_body: user_schema.Register, db: Session = Depends(get_db)):
    return user_crud.register_user(db, register_body)

# 4. 유저 정보 조회
@router.get("/users/{user_id}", response_model=user_schema.User)
async def user_info_get(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_crud.user_info_get(db, user_id)

# 5. 유저 정보 수정
@router.put("/users/{user_id}", response_model=user_schema.RegisterResponse)
async def user_info_revise(user_id: int, user_update:user_schema.Register, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_crud.user_info_revise(db, user_id, user_update)

# 6. 회원 탈퇴
@router.delete("/users/{user_id}", response_model=None)
async def user_quit(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user_crud.user_quit(db, user_id)

# 7-1. 유저의 개인그룹 리스트 조회
@router.get("/users/{user_id}/groups/private", response_model=user_schema.UserPrivateGroup)
async def user_private_group_list(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    private_group = user_crud.user_private_group_list(db, user_id)
    if private_group is None:
        raise HTTPException(status_code=404, detail="Private group not found")
    return private_group

# 7-2. 유저의 공유그룹 리스트 조회
@router.get("/users/{user_id}/groups/public", response_model=list[user_schema.UserPublicGroup])
async def user_public_group_list(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    public_group = user_crud.user_public_group_list(db, user_id)
    return public_group

