from sqlalchemy.orm import Session

import api.models.tables as tables
import api.schemas.post as post_schema

# 14. 포스트 올리기
def post_create(db: Session, post: post_schema.PostCreate) -> int:
    group_type = post.group_type
    group_id = post.group_id
    if group_type == "private":
        db_post = tables.Posts(creation_user_id=post.creation_user_id,
                              creation_date=post.creation_date,
                              post_header_path=post.post_header_path,
                              private_group_private_group_id=group_id,
                              public_group_public_group_id=None
                              )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post.post_id
    elif group_type == "public":
        db_post = tables.Posts(creation_user_id=post.creation_user_id,
                              creation_date=post.creation_date,
                              post_header_path=post.post_header_path,
                              private_group_private_group_id=None,
                              public_group_public_group_id=group_id
                              )
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post.post_id
    else:
        return None

# 그림 정보 업로드
def drawing_create(db: Session, drawing: post_schema.DrawingCreate) -> int:
    db_drawing = tables.Drawing(**drawing.dict())
    db.add(db_drawing)
    db.commit()
    db.refresh(db_drawing)
    return db_drawing.drawing_id


# 사진 정보 업로드
def picture_create(db: Session, picture: post_schema.PictureCreate) -> int:
    db_picture = tables.Picture(**picture.dict())
    db.add(db_picture)
    db.commit()
    db.refresh(db_picture)
    return db_picture.picture_id



# 15. 개별 포스트 정보 조회
def post_contents(db: Session, post_id: int) -> post_schema.Post:
    post = db.query(tables.Posts).filter(tables.Posts.post_id == post_id).first()
    post_id = post.post_id
    # 그림 정보 조회
    drawings = db.query(tables.Drawing).filter(tables.Drawing.posts_post_id == post_id).all()
    drawing_ids = [drawing.drawing_id for drawing in drawings]
    drawing_paths = [drawing.drawing_path for drawing in drawings]
    drawing_captions = [drawing.drawing_caption for drawing in drawings]
    drawing_orders = [drawing.drawing_order for drawing in drawings]
    # 사진 정보 조회
    pictures = db.query(tables.Picture).filter(tables.Picture.posts_post_id == post_id).all()
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
def post_revise(db: Session, post_id: int, drawing_id: int, post_update: post_schema.CaptionRevise) -> post_schema.CaptionReviseResponse:
    db_drawing = db.query(tables.Drawing).filter(tables.Drawing.drawing_id == drawing_id).first()
    if db_drawing:
        db_drawing.drawing_caption = post_update.new_caption
        db.commit()
        db.refresh(db_drawing)
    else:
        return None
    
    return post_schema.CaptionReviseResponse(new_caption=db_drawing.drawing_caption)


# 17. 개별 포스트 삭제
def post_delete(db: Session, post_id: int) -> None:
    post = db.query(tables.Posts).filter(tables.Posts.post_id == post_id).first()
    if post is None:
        return None
    db.delete(post)
    db.commit()
    return

