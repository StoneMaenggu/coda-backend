from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.group as group_crud
from api.db import get_db
import api.schemas.group as group_schema

router = APIRouter()

# 8-1. 개인 그룹 생성
@router.post("/group/private", response_model=group_schema.PrivateGroupCreateResponse)
async def private_group_create(group_body: group_schema.PrivateGroupCreate, db: AsyncSession = Depends(get_db)):
    return await group_crud.create_private_group(db, group_body)

# 8-2. 새 공유그룹 생성
@router.post("/group/public", response_model=group_schema.PublicGroupCreateResponse)
async def public_group_create(group_body: group_schema.PublicGroupCreate, db: AsyncSession = Depends(get_db)):
    result = await group_crud.create_public_group(db, group_body)
    result_master_user_id = result.master_user_id
    result_public_group_id = result.public_group_id
    await group_crud.update_user_has_public_group(db, user_id=result_master_user_id, public_group_id=result_public_group_id)
    
    await db.commit()  # 커밋 추가
    await db.refresh(result)
    return result

# 9. 그룹 유저 초대
@router.get("/groups/public/{public_group_id}/invite", response_model=group_schema.PublicGroupInviteResponse)
async def group_user_invite(public_group_id:int, db: AsyncSession = Depends(get_db)):
    result = await group_crud.group_user_invite(db, public_group_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Public group not found")
    return result

# 10. 기존 그룹 참여
@router.post("/groups/public/users/{user_id}/join", response_model=group_schema.PublicGroupJoinResponse)
async def group_user_join(user_id:int, join_body: group_schema.PublicGroupJoin, db: AsyncSession = Depends(get_db)):
    result = await group_crud.group_user_join(db, user_id, join=join_body)
    if result is None:
        raise HTTPException(status_code=404, detail="Access key or User ID not found")
    return result

# 11. 그룹 탈퇴
@router.delete("/groups/public/{public_group_id}/users/{user_id}", response_model=None)
async def group_user_quit(public_group_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    await group_crud.group_user_quit(db, public_group_id, user_id)
    return

# 12. 개인그룹 메인 화면 정보 조회
@router.get("/groups/private/{private_group_id}", response_model=list[group_schema.PrivateGroupPostResponse])
async def private_group_post_list(private_group_id: int, db: AsyncSession = Depends(get_db)):
    if await group_crud.get_private_group(db, private_group_id) is None:
        raise HTTPException(status_code=404, detail="Private group not found")
    posts = await group_crud.private_group_post_list(db, private_group_id)
    return posts

# 13. 공유그룹 메인 화면 정보 조회
@router.get("/groups/public/{public_group_id}", response_model=list[group_schema.PublicGroupPostResponse])
async def public_group_post_list(public_group_id: int, db: AsyncSession = Depends(get_db)):
    if await group_crud.get_public_group(db, public_group_id) is None:
        raise HTTPException(status_code=404, detail="Public group not found")
    posts = await group_crud.public_group_post_list(db, public_group_id)
    return posts
