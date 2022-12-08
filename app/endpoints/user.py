from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from fastapi.encoders import jsonable_encoder
from db.session import DbConnexionHandler


import crud, schemas
import deps
from core import security
from core.config import settings
from core.security import get_password_hash

from utils_ import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
    send_new_account_email,
    generate_password
)

router = APIRouter()

@router.post("/", response_model=schemas.UserUpdate)
def create_user(
    *,
    db: DbConnexionHandler = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    # current_user: schemas.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = crud.user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    return user
