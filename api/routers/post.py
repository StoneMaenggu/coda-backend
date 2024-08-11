from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import api.cruds.post as post_crud
from api.db import get_db

import api.schemas.post as post_schema

router = APIRouter()

# 14. 포스트 올리기
@router.post("/post", response_model=post_schema.PostCreateResponse)
async def post_create(post_body: post_schema.PostCreate, db: Session = Depends(get_db)):
    # post table
    post_id = post_crud.post_create(db, post_body)
    # picture table
    for i in range(len(post_body.picture_paths)):
        picture_data = post_schema.PictureCreate(
            posts_post_id=post_id,
            picture_path=post_body.picture_paths[i]
        )
        post_crud.picture_create(db, picture_data)
    
    # drawing table
    for i in range(len(post_body.drawing_paths)):
        drawing_data = post_schema.DrawingCreate(
            posts_post_id=post_id,
            drawing_path=post_body.drawing_paths[i],
            drawing_caption=post_body.drawing_captions[i],
            drawing_order=post_body.drawing_order[i]
        )
        post_crud.drawing_create(db, drawing_data)

    return post_schema.PostCreateResponse(post_id=post_id)

# 15. 개별 포스트 정보 조회
@router.get("/posts/{post_id}", response_model=post_schema.Post)
async def post_contents(post_id: int, db: Session = Depends(get_db)):
    return post_crud.post_contents(db, post_id)


# 16. 개별 포스트 수정
@router.patch("/posts/{post_id}/{drawing_id}", response_model=post_schema.CaptionReviseResponse)
async def post_revise(post_id: int, drawing_id: int, post_body: post_schema.CaptionRevise, db: Session = Depends(get_db)):
    result = post_crud.post_revise(db, post_id, drawing_id, post_body)
    if result is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return result

# 17. 개별 포스트 삭제
@router.delete("/posts/{post_id}", response_model=None)
async def post_delete(post_id: int, db: Session = Depends(get_db)):
    return post_crud.post_delete(db, post_id)

