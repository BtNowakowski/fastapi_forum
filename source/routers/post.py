from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from ..database import get_db, engine
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.Post])
def get_posts(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    print(current_user.id)
    print()
    new_post = models.Post(
        title=post.title, content=post.content, owner_id=current_user.id
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put("/{post_id}", response_model=schemas.Post)
def update_post(
    post_id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=404, detail=f"Post with id: {post_id} not found"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You don't have permission to update this post"
        )
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=404, detail=f"Post with id: {post_id} not found"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="You don't have permission to delete this post"
        )
    post_query.delete(synchronize_session=False)
    db.commit()


@router.get("/{post_id}", response_model=schemas.Post)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()
    if post == None:
        raise HTTPException(
            status_code=404, detail=f"Post with id: {post_id} not found"
        )
    return post
