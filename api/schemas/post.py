from pydantic import BaseModel, Field
import datetime
from typing import List

class PostBase(BaseModel):
    creation_user_id: int | None = Field(None, example=1)
    creation_date: datetime.date | None = Field(None, example="2024-01-01")


class PostCreate(PostBase):
    group_type: str | None = Field(None, example="private")
    group_id: int | None = Field(None, example=1)
    creation_user_id: int | None = Field(None, example=1)
    creation_date: datetime.date | None = Field(None, example="2024-01-01")

    picture_paths: List[str] | None = Field(None, example=["https://thisisforcoda.com/image/001", "https://thisisforcoda.com/image/002"])

    drawing_paths: List[str] | None = Field(None, example=["https://thisisforcoda.com/image/001", "https://thisisforcoda.com/image/002"])
    drawing_captions: List[str] | None = Field(None, example=["이 그림은 ...", "이 그림은 ..."])
    drawing_order: List[int] | None = Field(None, description="그림 순서를 의미하며, 초기 생성시 1부터 차례대로 번호를 매겨야 함", example=[1, 2])


# 그림 정보 생성
class DrawingCreate(BaseModel):
    posts_post_id: int | None = Field(None, example=1)
    drawing_path: str | None = Field(None, example="https://thisisforcoda.com/image/001")
    drawing_caption: str | None = Field(None, example="이 그림은 ...")
    drawing_order: int | None = Field(None, example=1)

class DrawingCreateResponse(DrawingCreate):
    drawing_id: int | None = Field(None, example=1)

    class Config:
        from_attributes = True

# 사진 정보 생성
class PictureCreate(BaseModel):
    posts_post_id: int | None = Field(None, example=1)
    picture_path: str | None = Field(None, example="https://thisisforcoda.com/image/001")

class PictureCreateResponse(PictureCreate):
    picture_id: int | None = Field(None, example=1)

    class Config:
        from_attributes = True

class PostCreateResponse(BaseModel):
    post_id: int | None = Field(None, example=1)

    class Config:
        from_attributes = True



# 15. 개별 포스트 정보 조회
class Post(PostBase):
    post_id: int | None = Field(None, example=1)
    post_header_path: List[str] | None = Field(None, example=["https://thisisforcoda.com/image/001", "https://thisisforcoda.com/image/002"])
    # 그림 정보 조회
    drawing_ids: List[int] | None = Field(None, example=[1, 2])
    drawing_paths: List[str] | None = Field(None, example=["https://thisisforcoda.com/image/001", "https://thisisforcoda.com/image/002"])
    drawing_captions: List[str] | None = Field(None, example=["이 그림은 ...", "이 그림은 ..."])
    drawing_orders: List[int] | None = Field(None, example=[1, 2])
    # 사진 정보 조회
    picture_ids: List[int] | None = Field(None, example=[1, 2])
    picture_paths: List[str] | None = Field(None, example=["https://thisisforcoda.com/image/001", "https://thisisforcoda.com/image/002"])

    class Config:
        from_attributes = True


# 16. 그림 캡션 수정
class CaptionRevise(BaseModel):
    new_caption: str | None = Field(None, example="이 그림은 ...")

class CaptionReviseResponse(CaptionRevise):
    pass

    class Config:
        from_attributes = True



