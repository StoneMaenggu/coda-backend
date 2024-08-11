from pydantic import BaseModel, Field

# 18. 포스트 별 리액션 보내기
class ReactionSend(BaseModel):
    reaction_user_id: int | None = Field(None, example=1)
    emoji_id: int | None = Field(None, example=1)

class ReactionSendResponse(ReactionSend):
    reaction_id: int | None = Field(None, example=1)

    class Config:
        orm_mode = True

# 19. 포스트 별 리액션 조회
class ReactionList(BaseModel):
    reaction_id: int | None = Field(None, example=1)
    reaction_user_id: int | None = Field(None, example=1)
    reaction_user_profile_path: str | None = Field(None, example="https://thisisforcoda.com/image/001")
    emoji_id: int | None = Field(None, example=1)

    class Config:
        orm_mode = True


