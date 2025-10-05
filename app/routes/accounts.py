from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, db, auth
from ..db import SessionLocal
from typing import List
from fastapi.security import OAuth2PasswordBearer
from ..auth import decode_token

router = APIRouter(prefix='/accounts', tags=['accounts'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def get_db():
    dbs = SessionLocal()
    try:
        yield dbs
    finally:
        dbs.close()

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload or not payload.sub:
        raise HTTPException(status_code=401, detail='Invalid auth')
    return int(payload.sub)

@router.post('/', response_model=schemas.AccountOut)
def create_account(account_in: schemas.AccountCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    acc = crud.create_account(db, user_id, account_in)
    return acc

@router.get('/', response_model=List[schemas.AccountOut])
def list_accounts(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    return crud.list_accounts(db, user_id)

@router.get('/{account_id}', response_model=schemas.AccountOut)
def get_account(account_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    acc = crud.get_account(db, user_id, account_id)
    if not acc:
        raise HTTPException(status_code=404, detail='Not found')
    return acc
