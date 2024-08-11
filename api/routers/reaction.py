from fastapi import APIRouter, Depends
import api.schemas.reaction as reaction_schema
from sqlalchemy.orm import Session

import api.cruds.reaction as reaction_cruds
from api.db import get_db

router = APIRouter()

# 18. 포스트 별 리액션 보내기
@router.post("/posts/{post_id}/reaction", response_model=reaction_schema.ReactionSendResponse)
async def reation_send(post_id:int, reaction_body: reaction_schema.ReactionSend, db: Session = Depends(get_db)):
    return reaction_cruds.reaction_send(db, post_id, reaction_body)

# 19. 포스트 별 리액션 조회
@router.get("/posts/{post_id}/reactions", response_model=list[reaction_schema.ReactionList])
async def reaction_list(post_id: int, db: Session = Depends(get_db)):
    return reaction_cruds.reaction_list(db, post_id)


# 20. 포스트 별 리액션 삭제하기
@router.delete("/posts/{post_id}/reactions/{reaction_id}", response_model=None)
async def reation_delete(post_id: int, reaction_id: int, db: Session = Depends(get_db)):
    return reaction_cruds.reaction_delete(db, post_id, reaction_id)


