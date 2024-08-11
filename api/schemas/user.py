
from pydantic import BaseModel, Field
import datetime

class UserBase(BaseModel):
    phone_num: str | None = Field(None, example="01012345678")
    user_password: str | None = Field(None, example="helloCODA!!")
    user_name: str | None = Field(None, example="홍길동")
    profile_path: str | None = Field(None, example="https://thisisforcoda.com/image/001")
    user_sex: bool | None = Field(None, description="True:man,False:woman")
    user_birth: datetime.date | None = Field(None, example="2024-01-01")
    user_text_available: bool | None = Field(True, example="True")

# 3. 회원 가입
class Register(UserBase):
    pass


class RegisterResponse(Register):
    user_id: int

    class Config:
        orm_mode = True

# 4. 유저 정보 조회
# 5. 유저 정보 수정
class User(UserBase):
    user_id: int

    class Config:
        orm_mode = True

# 7-1. 유저의 개인그룹 리스트 조회
class UserPrivateGroup(BaseModel):
    private_group_id: int | None = Field(None, example=1)
    private_group_header_path: str | None = Field(None, example="https://thisisforcoda.com/image/001")

    class Config:
        orm_mode = True

# 7-2. 유저의 공유그룹 리스트 조회
class UserPublicGroup(BaseModel):
    public_group_id: int | None = Field(None, example=1)
    public_group_name: str | None = Field(None, example="코다")
    public_group_header_path: str | None = Field(None, example="https://thisisforcoda.com/image/001")
    public_group_user_profiles: list[str] | None = Field(None, example=["https://thisisforcoda.com/image/001", "https://thisisforcoda.com/image/002"])

    class Config:
        orm_mode = True




