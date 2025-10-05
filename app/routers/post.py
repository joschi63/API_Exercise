from fastapi import Response, status, HTTPException, APIRouter, Depends

from sqlmodel import select
from ..database import SessionDep
from ..models.post_models import Post, PostCreate, PostUpdate, PostRead

from .. import token_managing as tm

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=list[PostRead])
def get_posts(session: SessionDep, current_user = Depends(tm.get_current_user)):
    posts = session.exec(select(Post).filter(Post.owner_id == current_user.id)).all()

    return posts

@router.get("/{id}", response_model=PostRead)
def get_post(id: int, session: SessionDep, current_user= Depends(tm.get_current_user)):
    post = session.get(Post, id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    return post

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostRead)
def create_post(post: PostCreate, session: SessionDep, current_user = Depends(tm.get_current_user)):
    
    post.owner_id = current_user.id
    new_post = Post.model_validate(post)
    
    session.add(new_post)
    session.commit()
    session.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, session: SessionDep, current_user = Depends(tm.get_current_user)):

    post = session.get(Post, id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    session.delete(post)
    session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=PostRead, status_code=status.HTTP_200_OK)
def update_post(id: int, post: PostUpdate, session: SessionDep, current_user = Depends(tm.get_current_user)):
    db_post = session.get(Post, id)

    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    db_post.sqlmodel_update(post.model_dump(exclude_unset=True))
    session.add(db_post)
    session.commit()
    session.refresh(db_post)

    return db_post
    