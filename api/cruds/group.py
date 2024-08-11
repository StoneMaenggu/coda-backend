from sqlalchemy.orm import Session

import api.models.tables as tables
import api.schemas.group as group_schema

import random

# 8-1. 개인 그룹 생성
def create_private_group(db: Session, group: group_schema.PrivateGroupCreate) -> tables.PrivateGroup:
    db_group = tables.PrivateGroup(**group.dict())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

# 8-2. 새 공유그룹 생성
def create_public_group(db: Session, group: group_schema.PublicGroupCreate) -> tables.PublicGroup:
    db_group = tables.PublicGroup(**group.dict(), num_users=1)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def update_user_has_public_group(db: Session, user_id:int, public_group_id: int) -> None:
    current_max_group_order_table = db.query(tables.UserHasPublicGroup.group_order).filter(tables.UserHasPublicGroup.user_user_id == user_id).order_by(tables.UserHasPublicGroup.group_order.desc()).first()
    if current_max_group_order_table is None:
        current_max_group_order = 0
    else:
        current_max_group_order = current_max_group_order_table[0]
    db_user_has_public_group = tables.UserHasPublicGroup(user_user_id=user_id,
                                                         public_group_public_group_id=public_group_id,
                                                         group_order = current_max_group_order + 1)
    db.add(db_user_has_public_group)
    db.commit()
    db.refresh(db_user_has_public_group)
    return 

# 9. 그룹 유저 초대
def group_user_invite(db: Session, invite:group_schema.PublicGroupInvite) -> group_schema.PublicGroupInviteResponse:
    public_group_check = db.query(tables.PublicGroup).filter(tables.PublicGroup.public_group_id == invite.public_group_id).first()
    if public_group_check is None:
        return None
    random_num = random.randint(100000, 999999)
    db_access_key = tables.GroupAccess(**invite.dict(), access_key=random_num)
    db.add(db_access_key)
    db.commit()
    db.refresh(db_access_key)
    return db_access_key

# 10. 기존 그룹 참여
def group_user_join(db: Session, user_id: int, join:group_schema.PublicGroupJoin) -> group_schema.PublicGroupJoinResponse:
    user_id_check = db.query(tables.User).filter(tables.User.user_id == user_id).first()
    if user_id_check is None:
        return None

    access_key_check = db.query(tables.GroupAccess).filter(tables.GroupAccess.access_key == join.access_key).first()
    if access_key_check is None:
        return None
    update_user_has_public_group(db, user_id, access_key_check.public_group_id)
    db.delete(access_key_check)

    num_users = db.query(tables.UserHasPublicGroup).filter(tables.UserHasPublicGroup.public_group_public_group_id == access_key_check.public_group_id).count()
    db.query(tables.PublicGroup).filter(tables.PublicGroup.public_group_id == access_key_check.public_group_id).update({tables.PublicGroup.num_users: num_users})
    db.commit()
    return group_schema.PublicGroupJoinResponse(user_id=user_id, public_group_id=access_key_check.public_group_id)

# 11. 그룹 탈퇴
def group_user_quit(db: Session, public_group_id: int, user_id: int) -> None:
    db.query(tables.UserHasPublicGroup).filter(tables.UserHasPublicGroup.user_user_id == user_id, tables.UserHasPublicGroup.public_group_public_group_id == public_group_id).delete()
    if db.query(tables.UserHasPublicGroup).filter(tables.UserHasPublicGroup.public_group_public_group_id == public_group_id).count() == 0:
        db.query(tables.PublicGroup).filter(tables.PublicGroup.public_group_id == public_group_id).delete()

    group = db.query(tables.PublicGroup).filter(tables.PublicGroup.public_group_id == public_group_id).first()
    num_users = db.query(tables.UserHasPublicGroup).filter(tables.UserHasPublicGroup.public_group_public_group_id == public_group_id).count()
    db.query(tables.PublicGroup).filter(tables.PublicGroup.public_group_id == public_group_id).update({tables.PublicGroup.num_users: num_users})
    db.commit()
    return group


# 12. 개인그룹 메인 화면 정보 조회
def private_group_post_list(db:Session, private_group_id: int) -> list[group_schema.PrivateGroupPostResponse]:
    db_posts = db.query(tables.Posts).filter(tables.Posts.private_group_private_group_id == private_group_id).all()
    posts = []
    for i in db_posts:
        posts.append(group_schema.PrivateGroupPostResponse(**i.__dict__))
    return posts


# 13. 공유그룹 메인 화면 정보 조회
def public_group_post_list(db:Session, public_group_id: int) -> list[group_schema.PublicGroupPostResponse]:
    db_posts = db.query(tables.Posts).filter(tables.Posts.public_group_public_group_id == public_group_id).all()
    posts = []
    for i in db_posts:
        posts.append(group_schema.PublicGroupPostResponse(**i.__dict__))
    return posts

def get_private_group(db:Session, private_group_id: int):
    return db.query(tables.PrivateGroup).filter(tables.PrivateGroup.private_group_id == private_group_id).first()

def get_public_group(db:Session, public_group_id: int):
    return db.query(tables.PublicGroup).filter(tables.PublicGroup.public_group_id == public_group_id).first()