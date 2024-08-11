from sqlalchemy.orm import Session

import api.models.tables as tables
import api.schemas.user as user_schema

# 3. 회원 가입
def register_user(db: Session, user: user_schema.Register) -> tables.User:
    db_user = tables.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 4. 유저 정보 조회
def user_info_get(db: Session, user_id: int) -> tables.User:
    user = db.query(tables.User).filter(tables.User.user_id == user_id).first()
    return user

# 5. 유저 정보 수정
def get_user(db: Session, user_id: int):
    return db.query(tables.User).filter(tables.User.user_id == user_id).first()

def user_info_revise(db: Session, user_id: int, user_update: user_schema.Register) -> tables.User:
    db_user = get_user(db, user_id)
    if db_user:
        db_user.phone_num = user_update.phone_num
        db_user.user_password = user_update.user_password
        db_user.user_name = user_update.user_name
        db_user.profile_path = user_update.profile_path
        db_user.user_birth = user_update.user_birth
        db_user.user_text_available = user_update.user_text_available
        db_user.user_sex = user_update.user_sex
        db.commit()
        db.refresh(db_user)
    return db_user

# 6. 회원 탈퇴
def user_quit(db: Session, user_id: int) -> None:
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()

# 7-1. 유저의 개인그룹 리스트 조회
def user_private_group_list(db: Session, user_id: int) -> user_schema.UserPrivateGroup:
    private_group = db.query(tables.PrivateGroup).filter(tables.PrivateGroup.user_user_id == user_id).first()
    return private_group

# 7-2. 유저의 공유그룹 리스트 조회
def user_public_group_list(db: Session, user_id: int) -> list[user_schema.UserPublicGroup]:
    user_ = db.query(tables.UserHasPublicGroup).filter(tables.UserHasPublicGroup.user_user_id == user_id).all()
    public_group = []
    for i in user_:
        public_group.append(i.public_group)
    return public_group

