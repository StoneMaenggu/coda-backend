from sqlalchemy.orm import Session

import api.models.tables as tables
import api.schemas.post as post_schema

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession



# 14. 포스트 올리기
async def post_create(db: AsyncSession, post: post_schema.PostCreate) -> int:
    group_type = post.group_type
    group_id = post.group_id
    if group_type == "private":
        db_post = tables.Posts(
            creation_user_id=post.creation_user_id,
            creation_date=post.creation_date,
            post_header_path=post.post_header_path,
            private_group_private_group_id=group_id,
            public_group_public_group_id=None
        )
    elif group_type == "public":
        db_post = tables.Posts(
            creation_user_id=post.creation_user_id,
            creation_date=post.creation_date,
            post_header_path=post.post_header_path,
            private_group_private_group_id=None,
            public_group_public_group_id=group_id
        )
    else:
        return None

    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post.post_id


# 그림 정보 업로드
async def drawing_create(db: AsyncSession, drawing: post_schema.DrawingCreate) -> int:
    db_drawing = tables.Drawing(**drawing.dict())
    db.add(db_drawing)
    await db.commit()
    await db.refresh(db_drawing)
    return db_drawing.drawing_id


# 사진 정보 업로드
async def picture_create(db: AsyncSession, picture: post_schema.PictureCreate) -> int:
    db_picture = tables.Picture(**picture.dict())
    db.add(db_picture)
    await db.commit()
    await db.refresh(db_picture)
    return db_picture.picture_id


# 15. 개별 포스트 정보 조회
async def post_contents(db: AsyncSession, post_id: int) -> post_schema.Post:
    stmt = select(tables.Posts).filter(tables.Posts.post_id == post_id)
    result = await db.execute(stmt)
    post = result.scalars().first()

    if post is None:
        return None

    # 그림 정보 조회
    stmt = select(tables.Drawing).filter(tables.Drawing.posts_post_id == post.post_id)
    result = await db.execute(stmt)
    drawings = result.scalars().all()
    drawing_ids = [drawing.drawing_id for drawing in drawings]
    drawing_paths = [drawing.drawing_path for drawing in drawings]
    drawing_captions = [drawing.drawing_caption for drawing in drawings]
    drawing_orders = [drawing.drawing_order for drawing in drawings]

    # 사진 정보 조회
    stmt = select(tables.Picture).filter(tables.Picture.posts_post_id == post.post_id)
    result = await db.execute(stmt)
    pictures = result.scalars().all()
    picture_ids = [picture.picture_id for picture in pictures]
    picture_paths = [picture.picture_path for picture in pictures]

    result = post_schema.Post(
        post_id=post_id,
        creation_user_id=post.creation_user_id,
        creation_date=post.creation_date,
        post_header_path=post.post_header_path,
        drawing_ids=drawing_ids,
        drawing_paths=drawing_paths,
        drawing_captions=drawing_captions,
        drawing_orders=drawing_orders,
        picture_ids=picture_ids,
        picture_paths=picture_paths
    )
    return result


# 16. 개별 포스트 수정
async def post_revise(db: AsyncSession, post_id: int, drawing_id: int, post_update: post_schema.CaptionRevise) -> post_schema.CaptionReviseResponse:
    stmt = select(tables.Drawing).filter(tables.Drawing.drawing_id == drawing_id)
    result = await db.execute(stmt)
    db_drawing = result.scalars().first()

    if db_drawing:
        db_drawing.drawing_caption = post_update.new_caption
        await db.commit()
        await db.refresh(db_drawing)
        return post_schema.CaptionReviseResponse(new_caption=db_drawing.drawing_caption)
    else:
        return None


# 17. 개별 포스트 삭제
async def post_delete(db: AsyncSession, post_id: int) -> None:
    stmt = select(tables.Posts).filter(tables.Posts.post_id == post_id)
    result = await db.execute(stmt)
    post = result.scalars().first()

    if post is None:
        return None

    await db.delete(post)
    await db.commit()
    return