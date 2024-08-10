from fastapi import APIRouter
import api.schemas.post as post_schema

router = APIRouter()

# 14. 포스트 올리기
@router.post("/post", response_model=post_schema.PostCreateResponse)
async def post_create(post_body: post_schema.PostCreate):
    return post_schema.PostCreateResponse(post_id=1, picture_ids=[1,2], drawing_ids=[1,2], **post_body.dict())

# 15. 개별 포스트 정보 조회
@router.get("/posts/{post_id}", response_model=post_schema.Post)
async def post_contents(post_id: int):
    return post_schema.Post(post_id=post_id,
                            picture_ids=[1,2],
                            drawing_ids=[1,2],
                            creation_user_id=1,
                            creation_date="2024-01-01",
                            post_header_path="https://thisisforcoda.com/image/001",
                            picture_paths=["https://thisisforcoda.com/image/001", "https://thisisforcoda.com/image/002"],
                            drawing_paths=["https://thisisforcoda.com/image/001", "https://thisisforcoda.com/image/002"],
                            drawing_captions=["이 그림은 ...", "이 그림은 ..."],
                            drawing_order=[1, 2])

# 16. 개별 포스트 수정
@router.patch("/posts/{post_id}/{drawing_id}", response_model=post_schema.PostReviseResponse)
async def post_revise(post_id: int, drawing_id: int, post_body: post_schema.PostRevise):
    return post_schema.PostReviseResponse(new_caption="이 그림은 ...")

# 17. 개별 포스트 삭제
@router.delete("/posts/{post_id}")
async def post_delete(post_id: int):
    return

