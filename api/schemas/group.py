from pydantic import BaseModel, Field

# 8. 새 공유그룹 생성
class PublicGroupBase(BaseModel):
    master_user_id: int | None = Field(None, example=1)
    public_group_name: str | None = Field(None, example="코다")
    public_group_header_path: str | None = Field(None, example="https://thisisforcoda.com/image/001")

class PublicGroupCreate(PublicGroupBase):
    pass

class PublicGroupCreateResponse(PublicGroupCreate):
    public_group_id: int

    class Config:
        orm_mode = True

# 9. 그룹 유저 초대
class PublicGroupInvite(BaseModel):
    public_group_id: int | None = Field(None, example=1)


class PublicGroupInviteResponse(PublicGroupInvite):
    access_key: str | None = Field(None, example="123456")

    class Config:
        orm_mode = True


# 10. 기존 그룹 참여
class PublicGroupJoin(BaseModel):
    access_key: str | None = Field(None, example="123456")

class PublicGroupJoinResponse(BaseModel):
    user_id: int | None = Field(None, example=1)
    public_group_id: int | None = Field(None, example=1)

    class Config:
        orm_mode = True


# 포스트 정보
class PostBase(BaseModel):
    post_id: int | None = Field(None, example=1)
    creation_user_id: int | None = Field(None, example=1)
    creation_date: str | None = Field(None, example="2024-01-01")
    post_header_path: str | None = Field(None, example="https://thisisforcoda.com/image/001")

# 12. 개인그룹 메인 화면 정보 조회
class PrivateGroupPostResponse(PostBase):
    private_group_id: int | None = Field(None, example=1)

    class Config:
        orm_mode = True

# 13. 공유그룹 메인 화면 정보 조회
class PublicGroupPostResponse(PostBase):
    public_group_id: int | None = Field(None, example=1)

    class Config:
        orm_mode = True

