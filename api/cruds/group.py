from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func  # Add this line to import the func function
import api.models.tables as tables
import api.schemas.group as group_schema
from sqlalchemy.orm import joinedload
import json


import random

# 8-1. 개인 그룹 생성
async def create_private_group(db: AsyncSession, group: group_schema.PrivateGroupCreate) -> tables.PrivateGroup:
    db_group = tables.PrivateGroup(**group.dict())
    db.add(db_group)
    await db.commit()
    await db.refresh(db_group)
    return db_group

# 8-2. 새 공유그룹 생성
async def create_public_group(db: AsyncSession, group: group_schema.PublicGroupCreate) -> tables.PublicGroup:
    db_group = tables.PublicGroup(**group.dict(), num_users=1)
    db.add(db_group)
    await db.commit()
    await db.refresh(db_group)
    return db_group

async def update_user_has_public_group(db: AsyncSession, user_id:int, public_group_id: int) -> None:
    stmt = select(tables.UserHasPublicGroup.group_order).filter(tables.UserHasPublicGroup.user_user_id == user_id).order_by(tables.UserHasPublicGroup.group_order.desc())
    result = await db.execute(stmt)
    current_max_group_order = result.scalar()  # 단일 스칼라 값 가져오기

    if current_max_group_order is None:
        current_max_group_order = 0

    db_user_has_public_group = tables.UserHasPublicGroup(
        user_user_id=user_id,
        public_group_public_group_id=public_group_id,
        group_order=current_max_group_order + 1
    )
    
    db.add(db_user_has_public_group)
    await db.commit()
    await db.refresh(db_user_has_public_group)
    return

# 9. 그룹 유저 초대
async def group_user_invite(db: AsyncSession, public_group_id) -> group_schema.PublicGroupInviteResponse:
    stmt = select(tables.PublicGroup).filter(tables.PublicGroup.public_group_id == public_group_id)
    result = await db.execute(stmt)
    public_group_check = result.scalars().first()

    if public_group_check is None:
        return None
    
    random_num = random.randint(100000, 999999)
    db_access_key = tables.GroupAccess(public_group_id=public_group_id, access_key=random_num)
    db.add(db_access_key)
    await db.commit()
    await db.refresh(db_access_key)
    return db_access_key

# 10. 기존 그룹 참여
async def group_user_join(db: AsyncSession, user_id: int, join: group_schema.PublicGroupJoin) -> group_schema.PublicGroupJoinResponse:
    stmt = select(tables.User).filter(tables.User.user_id == user_id)
    result = await db.execute(stmt)
    user_id_check = result.scalars().first()

    if user_id_check is None:
        return None

    stmt = select(tables.GroupAccess).filter(tables.GroupAccess.access_key == join.access_key)
    result = await db.execute(stmt)
    access_key_check = result.scalars().first()

    if access_key_check is None:
        return None
    
    await update_user_has_public_group(db, user_id, access_key_check.public_group_id)

    # 비동기적으로 삭제 작업 처리
    await db.delete(access_key_check)
    await db.commit()

    # 유저 그룹 수 업데이트 (여기서 객체가 아닌 실제 숫자를 반환해야 합니다.)
    stmt = select(func.count(tables.UserHasPublicGroup.user_user_id)).filter(
        tables.UserHasPublicGroup.public_group_public_group_id == access_key_check.public_group_id
    )
    num_users = await db.scalar(stmt)  # 유저 수를 정확히 카운트하여 정수로 반환

    # 공개 그룹 갱신
    await db.execute(
        tables.PublicGroup.__table__.update()
        .where(tables.PublicGroup.public_group_id == access_key_check.public_group_id)
        .values(num_users=num_users)
    )
    
    await db.commit()
    return group_schema.PublicGroupJoinResponse(user_id=user_id, public_group_id=access_key_check.public_group_id)



# 11. 그룹 탈퇴
from sqlalchemy import delete

async def group_user_quit(db: AsyncSession, public_group_id: int, user_id: int) -> None:
    # 특정 사용자와 그룹에 해당하는 UserHasPublicGroup 레코드를 삭제
    stmt = delete(tables.UserHasPublicGroup).where(
        tables.UserHasPublicGroup.user_user_id == user_id,
        tables.UserHasPublicGroup.public_group_public_group_id == public_group_id
    )
    await db.execute(stmt)

    # 삭제 후에 해당 public_group_id에 속한 사용자가 더 이상 없는지 확인
    stmt = select(func.count(tables.UserHasPublicGroup.user_user_id)).filter(
        tables.UserHasPublicGroup.public_group_public_group_id == public_group_id
    )
    num_users = await db.scalar(stmt)

    if num_users == 0:
        # 사용자가 더 이상 없다면 해당 PublicGroup을 삭제
        stmt = delete(tables.PublicGroup).where(
            tables.PublicGroup.public_group_id == public_group_id
        )
        await db.execute(stmt)

    # 그룹의 사용자 수 업데이트
    stmt = (
        tables.PublicGroup.__table__.update()
        .where(tables.PublicGroup.public_group_id == public_group_id)
        .values(num_users=num_users)
    )
    await db.execute(stmt)
    await db.commit()
    return



# 개인그룹 메인 화면 정보 조회
async def private_group_post_list(db: AsyncSession, private_group_id: int) -> list[group_schema.PrivateGroupPostResponse]:
    stmt = select(tables.Posts).filter(tables.Posts.private_group_private_group_id == private_group_id).options(joinedload(tables.Posts.drawings))
    result = await db.execute(stmt)
    db_posts = result.unique().scalars().all()

    posts = []
    for post in db_posts:
        post_dict = post.__dict__.copy()
        posts.append(group_schema.PrivateGroupPostResponse(**post_dict))  # 리스트 그대로 반환

    return posts

# 공유그룹 메인 화면 정보 조회
async def public_group_post_list(db: AsyncSession, public_group_id: int) -> list[group_schema.PublicGroupPostResponse]:
    stmt = select(tables.Posts).filter(tables.Posts.public_group_public_group_id == public_group_id).options(joinedload(tables.Posts.drawings))
    result = await db.execute(stmt)
    db_posts = result.unique().scalars().all()

    posts = []
    for post in db_posts:
        post_dict = post.__dict__.copy()
        posts.append(group_schema.PublicGroupPostResponse(**post_dict))  # 리스트 그대로 반환

    return posts




async def get_private_group(db: AsyncSession, private_group_id: int):
    stmt = select(tables.PrivateGroup).filter(tables.PrivateGroup.private_group_id == private_group_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_public_group(db: AsyncSession, public_group_id: int):
    stmt = select(tables.PublicGroup).filter(tables.PublicGroup.public_group_id == public_group_id)
    result = await db.execute(stmt)
    return result.scalars().first()