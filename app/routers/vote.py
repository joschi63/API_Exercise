from fastapi import status, HTTPException, APIRouter, Depends

from sqlmodel import select
from ..database import SessionDep
from .. import token_managing as tm
from ..models.votes_models import VoteCreate, Vote
from ..models.post_models import Post

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: VoteCreate, session: SessionDep, current_user=Depends(tm.get_current_user)):

    post = session.exec(select(Post).where(Post.id == vote.post_id)).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {vote.post_id} does not exist")
    
    if post.owner_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Users cannot vote on their own posts")

    vote_query = session.exec(select(Vote).
                                 where(Vote.post_id == vote.post_id, Vote.user_id == current_user.id))
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        
        new_vote = Vote(post_id=vote.post_id, user_id=current_user.id)
        session.add(new_vote)
        session.commit()
        
        return {"message": "successfully added vote"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
        session.delete(found_vote)
        session.commit()
        
        return {"message": "successfully deleted vote"}