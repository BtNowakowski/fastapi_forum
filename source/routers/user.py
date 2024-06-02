from fastapi import FastAPI, Depends, HTTPException, status, Response, APIRouter
from ..database import get_db, engine
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    new_user = models.User(
        username=user.username, email=user.email, password=user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.User,
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user == None:
        raise HTTPException(
            status_code=404, detail=f"User with id: {user_id} not found"
        )
    return user
