from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, crud, db
from ..db import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from ..auth import decode_token

router = APIRouter(prefix='/transactions', tags=['transactions'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def get_db():
    dbs = SessionLocal();
    try: yield dbs
    finally: dbs.close()

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload or not payload.sub:
        raise HTTPException(status_code=401, detail='Invalid auth')
    return int(payload.sub)

@router.post('/', response_model=schemas.TransactionOut)
def create_transaction(tx_in: schemas.TransactionCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    tx = crud.create_transaction(db, user_id, tx_in)
    return tx

@router.get('/', response_model=List[schemas.TransactionOut])
def list_transactions(account_id: Optional[int] = None, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    return crud.list_transactions(db, user_id, account_id)
