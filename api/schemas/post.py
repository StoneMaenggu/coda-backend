from pydantic import BaseModel, Field

class PostBase(BaseModel):
    creation_user_id: int | None = Field(None, example=1)
    creation_date: str | None = Field(None, example="2024-01-01")

# 14. 포스트 올리기
class PostCreate(PostBase):
    post_header_path: str | None = Field(None, example="https://thisisforcoda.com/image/001")
    picture_paths: list[str] | None = Field(None, example=["https://thisisforcoda.com/image/001", "https://thisisforcoda.com/image/002"])
    drawing_paths: list[str] | None = Field(None, example=["https://thisisforcoda.com/image/001", "https://thisisforcoda.com/image/002"])
    drawing_captions: list[str] | None = Field(None, example=["이 그림은 ...", "이 그림은 ..."])
    drawing_order: list[int] | None = Field(None, description="그림 순서를 의미하며, 초기 생성시 1부터 차례대로 번호를 매겨야 함", example=[1, 2])

class PostCreateResponse(PostCreate):
    post_id: int | None = Field(None, example=1)
    picture_ids: list[int] | None = Field(None, example=[1, 2])
    drawing_ids: list[int] | None = Field(None, description="입력받은 순서대로 반환", example=[1, 2])

    class Config:
        orm_mode = True

# 15. 개별 포스트 정보 조회
class Post(PostCreate):
    post_id: int | None = Field(None, example=1)
    picture_ids: list[int] | None = Field(None, example=[1, 2])
    drawing_ids: list[int] | None = Field(None, example=[1, 2])

    class Config:
        orm_mode = True

# 16. 개별 포스트 수정
class PostRevise(BaseModel):
    new_caption: str | None = Field(None, example="이 그림은 ...")

class PostReviseResponse(PostRevise):
    pass

    class Config:
        orm_mode = True



