from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud, db, auth
from ..db import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm
from ..auth import create_access_token, decode_token

router = APIRouter(prefix='/auth', tags=['auth'])

def get_db():
    dbs = SessionLocal()
    try:
        yield dbs
    finally:
        dbs.close()

@router.post('/register', response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail='Email already registered')
    user = crud.create_user(db, user_in.email, user_in.password)
    return user

@router.post('/login', response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_access_token(subject=user.id)
    return {'access_token': token, 'token_type': 'bearer'}
