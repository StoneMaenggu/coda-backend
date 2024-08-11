from sqlalchemy.orm import Session

import api.models.tables as tables
import api.schemas.reaction as reaction_schema


# 18. 포스트 별 리액션 보내기
def reaction_send(db: Session, post_id: int, reaction: reaction_schema.ReactionSend) -> reaction_schema.ReactionSendResponse:
    db_reaction = tables.Reaction(posts_post_id=post_id, **reaction.dict())
    db.add(db_reaction)
    db.commit()
    db.refresh(db_reaction)
    return db_reaction

# 19. 포스트 별 리액션 조회
def reaction_list(db: Session, post_id: int) -> list[reaction_schema.ReactionList]:
    reactions = db.query(tables.Reaction).filter(tables.Reaction.posts_post_id == post_id).all()
    reaction_user_profile_path = db.query(tables.User.profile_path).filter(tables.User.user_id == tables.Reaction.reaction_user_id).first()
    return [reaction_schema.ReactionList(**reaction.__dict__, reaction_user_profile_path=reaction_user_profile_path.profile_path) for reaction in reactions]

# 20. 포스트 별 리액션 삭제하기
def reaction_delete(db: Session, post_id: int, reaction_id: int):
    reaction = db.query(tables.Reaction).filter(tables.Reaction.posts_post_id == post_id, tables.Reaction.reaction_id == reaction_id).first()
    if reaction is None:
        return None
    db.delete(reaction)
    db.commit()
    return None