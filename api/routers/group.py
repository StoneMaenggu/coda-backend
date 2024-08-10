from fastapi import APIRouter
import api.schemas.group as group_schema

router = APIRouter()

# 8. 새 공유그룹 생성
@router.post("/group", response_model=group_schema.PublicGroupCreateResponse)
async def group_create(group_body: group_schema.PublicGroupCreate):
    return group_schema.PublicGroupCreateResponse(public_group_id=1, **group_body.dict())

# 9. 그룹 유저 초대
@router.post("/groups/public/{public_group_id}/invite", response_model=group_schema.PublicGroupInviteResponse)
async def group_user_invite(public_group_id: int):
    return group_schema.PublicGroupInviteResponse(public_group_id=public_group_id, access_key="123456")

# 10. 기존 그룹 참여
@router.post("/groups/public/users/{user_id}/join", response_model=group_schema.PublicGroupJoinResponse)
async def group_user_join(user_id:int, join_body: group_schema.PublicGroupJoin):
    return group_schema.PublicGroupJoinResponse(user_id=1, public_group_id=1)

# 11. 그룹 탈퇴
@router.delete("/groups/public/{public_group_id}/users/{user_id}")
async def group_user_quit(public_group_id: int, user_id: int):
    return

# 12. 개인그룹 메인 화면 정보 조회
@router.get("/groups/private/{private_group_id}", response_model=list[group_schema.PrivateGroupPostResponse])
async def private_group_post_list(private_group_id: int):
    return [group_schema.PrivateGroupPostResponse(private_group_id=private_group_id,
                                                post_id=1,
                                                creation_user_id=1,
                                                creation_date="2024-01-01",
                                                post_header_path="https://thisisforcoda.com/image/001")]

# 13. 공유그룹 메인 화면 정보 조회
@router.get("/groups/public/{public_group_id}", response_model=list[group_schema.PublicGroupPostResponse])
async def public_group_post_list(public_group_id: int):
    return [group_schema.PublicGroupPostResponse(public_group_id=public_group_id,
                                                post_id=1,
                                                creation_user_id=1,
                                                creation_date="2024-01-01",
                                                post_header_path="https://thisisforcoda.com/image/001")]
