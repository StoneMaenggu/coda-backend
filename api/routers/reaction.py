from fastapi import APIRouter
import api.schemas.reaction as reaction_schema

router = APIRouter()

# 18. 포스트 별 리액션 보내기
@router.post("/posts/{post_id}/reaction", response_model=reaction_schema.ReactionSendResponse)
async def reation_send(post_id:int, reaction_body: reaction_schema.ReactionSend):
    return reaction_schema.ReactionSendResponse(reaction_id=1, **reaction_body.dict())

# 19. 포스트 별 리액션 조회
@router.get("/posts/{post_id}/reactions", response_model=list[reaction_schema.ReactionList])
async def reaction_list(post_id: int):
    return [reaction_schema.ReactionList(reaction_id=1,
                                        reaction_user_id=1,
                                        reaction_user_profile_path="https://thisisforcoda.com/image/001",
                                        emoji_id=1,
                                        emoji_path="https://thisisforcoda.com/image/001")]


# 20. 포스트 별 리액션 삭제하기
@router.delete("/posts/{post_id}/reactions/{reaction_id}")
async def reation_delete(post_id: int, reaction_id: int):
    pass


