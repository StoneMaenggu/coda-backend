from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
import api.models.tables as tables
import api.schemas.user as user_schema

# 3. 회원 가입
async def register_user(db: AsyncSession, user: user_schema.Register) -> tables.User:
    db_user = tables.User(**user.dict())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# 4. 유저 정보 조회
async def user_info_get(db: AsyncSession, user_id: int) -> tables.User:
    stmt = select(tables.User).filter(tables.User.user_id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    return user

# 5. 유저 정보 수정
async def get_user(db: AsyncSession, user_id: int):
    stmt = select(tables.User).filter(tables.User.user_id == user_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def user_info_revise(db: AsyncSession, user_id: int, user_update: user_schema.Register) -> tables.User:
    db_user = await get_user(db, user_id)
    if db_user:
        db_user.phone_num = user_update.phone_num
        db_user.user_password = user_update.user_password
        db_user.user_name = user_update.user_name
        db_user.profile_path = user_update.profile_path
        db_user.user_birth = user_update.user_birth
        db_user.user_text_available = user_update.user_text_available
        db_user.user_sex = user_update.user_sex
        await db.commit()
        await db.refresh(db_user)
    return db_user

# 6. 회원 탈퇴
async def user_quit(db: AsyncSession, user_id: int) -> None:
    # 1. 사용자 정보를 가져옵니다.
    db_user = await get_user(db, user_id)
    
    if db_user:
        # 2. 해당 사용자가 속한 모든 public_group_id를 가져옵니다.
        stmt = select(tables.UserHasPublicGroup.public_group_public_group_id).filter(
            tables.UserHasPublicGroup.user_user_id == user_id
        )
        result = await db.execute(stmt)
        public_group_ids = result.scalars().all()
        
        # 3. 사용자를 삭제합니다. 이때 `cascade`에 의해 `user_has_public_group`이 자동으로 삭제됩니다.
        await db.delete(db_user)
        await db.commit()

        # 4. 각 public_group_id에 대해 num_users를 업데이트하고, num_users가 0이면 해당 public_group을 삭제합니다.
        for public_group_id in public_group_ids:
            # num_users를 업데이트합니다.
            stmt = select(func.count(tables.UserHasPublicGroup.user_user_id)).filter(
                tables.UserHasPublicGroup.public_group_public_group_id == public_group_id
            )
            num_users = await db.scalar(stmt)

            if num_users == 0:
                # num_users가 0이면 해당 public_group을 삭제합니다.
                stmt = delete(tables.PublicGroup).where(
                    tables.PublicGroup.public_group_id == public_group_id
                )
                await db.execute(stmt)
            else:
                # num_users를 업데이트합니다.
                stmt = (
                    tables.PublicGroup.__table__.update()
                    .where(tables.PublicGroup.public_group_id == public_group_id)
                    .values(num_users=num_users)
                )
                await db.execute(stmt)

        await db.commit()

# 7-1. 유저의 개인그룹 리스트 조회
async def user_private_group_list(db: AsyncSession, user_id: int) -> user_schema.UserPrivateGroup:
    stmt = select(tables.PrivateGroup).filter(tables.PrivateGroup.user_user_id == user_id)
    result = await db.execute(stmt)
    private_group = result.scalars().first()
    return private_group

# 7-2. 유저의 공유그룹 리스트 조회
async def user_public_group_list(db: AsyncSession, user_id: int) -> list[user_schema.UserPublicGroup]:
    stmt = select(tables.UserHasPublicGroup).filter(tables.UserHasPublicGroup.user_user_id == user_id)
    result = await db.execute(stmt)
    user_ = result.scalars().all()
    public_group = [i.public_group for i in user_]
    return public_group

