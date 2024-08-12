from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import api.models.tables as tables
import api.schemas.reaction as reaction_schema



# 18. 포스트 별 리액션 보내기
async def reaction_send(db: AsyncSession, post_id: int, reaction: reaction_schema.ReactionSend) -> reaction_schema.ReactionSendResponse:
    db_reaction = tables.Reaction(posts_post_id=post_id, **reaction.dict())
    db.add(db_reaction)
    await db.commit()
    await db.refresh(db_reaction)
    return db_reaction

# 19. 포스트 별 리액션 조회
async def reaction_list(db: AsyncSession, post_id: int) -> list[reaction_schema.ReactionList]:
    stmt = select(tables.Reaction).filter(tables.Reaction.posts_post_id == post_id)
    result = await db.execute(stmt)
    reactions = result.scalars().all()

    reaction_list = []
    for reaction in reactions:
        stmt = select(tables.User.profile_path).filter(tables.User.user_id == reaction.reaction_user_id)
        result = await db.execute(stmt)
        reaction_user_profile_path = result.scalar()
        
        reaction_list.append(
            reaction_schema.ReactionList(
                **reaction.__dict__,
                reaction_user_profile_path=reaction_user_profile_path
            )
        )
    return reaction_list

# 20. 포스트 별 리액션 삭제하기
async def reaction_delete(db: AsyncSession, post_id: int, reaction_id: int):
    stmt = select(tables.Reaction).filter(
        tables.Reaction.posts_post_id == post_id,
        tables.Reaction.reaction_id == reaction_id
    )
    result = await db.execute(stmt)
    reaction = result.scalars().first()

    if reaction is None:
        return None

    await db.delete(reaction)
    await db.commit()
    return None