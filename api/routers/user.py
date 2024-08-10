from fastapi import APIRouter
import api.schemas.user as user_schema
router = APIRouter()


# 3. 회원 가입
@router.post("/register",response_model=user_schema.RegisterResponse)
async def register(register_body: user_schema.Register):
    return user_schema.RegisterResponse(user_id=1, private_group_id=1, **register_body.dict())

# 4. 유저 정보 조회
@router.get("/users/{user_id}", response_model=user_schema.User)
async def user_info_get(user_id: int):
    return user_schema.User(user_id=user_id,
                            phone_num="01012345678",
                            user_password="helloCODA!!",
                            user_name="홍길동",
                            profile_path="https://thisisforcoda.com/image/001",
                            user_sex=True,
                            user_birth="2024-01-01",
                            user_text_available=True)

# 5. 유저 정보 수정
@router.put("/users/{user_id}", response_model=user_schema.User)
async def user_info_revise(user_id: int, user_body:user_schema.Register):
    return user_schema.User(user_id=user_id, **user_body.dict())

# 6. 회원 탈퇴
@router.delete("/users/{user_id}")
async def user_quit(user_id: int):
    return

# 7-1. 유저의 개인그룹 리스트 조회
@router.get("/users/{user_id}/groups/private", response_model=user_schema.UserPrivateGroup)
async def user_private_group_list(user_id: int):
    return user_schema.UserPrivateGroup(private_group_id=1, private_group_header_path="https://thisisforcoda.com/image/001")

# 7-2. 유저의 공유그룹 리스트 조회
@router.get("/users/{user_id}/groups/public", response_model=list[user_schema.UserPublicGroup])
async def user_public_group_list(user_id: int):
    return [user_schema.UserPublicGroup(public_group_id=1,
                                        public_group_header_path="https://thisisforcoda.com/image/001",
                                        public_group_user_profiles=["https://thisisforcoda.com/image/001", "https://thisisforcoda.com/image/002"])]

