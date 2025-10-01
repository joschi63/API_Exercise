from fastapi import Response, status, HTTPException, APIRouter

from sqlmodel import select
from ..database import SessionDep
from ..models.post_models import Post, PostCreate, PostUpdate, PostRead

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=list[PostRead])
def get_posts(session: SessionDep):
    posts = session.exec(select(Post)).all()

    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostRead)
def create_post(post: PostCreate, session: SessionDep):
    new_post = Post.model_validate(post)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=PostRead)
def get_post(id: int, session: SessionDep):
    post = session.get(Post, id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, session: SessionDep):
    post = session.get(Post, id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    session.delete(post)
    session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=PostRead, status_code=status.HTTP_200_OK)
def update_post(id: int, post: PostUpdate, session: SessionDep):
    db_post = session.get(Post, id)

    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    db_post.sqlmodel_update(post.model_dump(exclude_unset=True))
    session.add(db_post)
    session.commit()
    session.refresh(db_post)

    return db_post