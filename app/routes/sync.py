from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
from ..db import SessionLocal
from ..auth import decode_token
from fastapi.security import OAuth2PasswordBearer
from .. import crud

router = APIRouter(prefix='/sync', tags=['sync'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    if not payload or not payload.sub:
        raise HTTPException(status_code=401, detail='Invalid auth')
    return int(payload.sub)

@router.post('/push')
def sync_push(payload: Dict[Any, Any], user_id: int = Depends(get_current_user)):
    db = SessionLocal()
    try:
        accounts = payload.get('accounts', [])
        txs = payload.get('transactions', [])
        acc_out = crud.upsert_accounts(db, user_id, accounts)
        tx_out = crud.upsert_transactions(db, user_id, txs)
        return {'accounts': [dict(id=a.id, name=a.name) for a in acc_out], 'transactions': [dict(id=t.id) for t in tx_out]}
    finally:
        db.close()

@router.get('/pull')
def sync_pull(since: int = 0, user_id: int = Depends(get_current_user)):
    db = SessionLocal()
    try:
        accounts = crud.list_accounts(db, user_id)
        txs = crud.list_transactions(db, user_id)
        return {'accounts': [dict(id=a.id, name=a.name, manual_balance=a.manual_balance, manual_override=a.manual_override, currency=a.currency, notes=a.notes) for a in accounts], 'transactions': [dict(id=t.id, account_id=t.account_id, tx_type=t.tx_type, amount=t.amount, currency=t.currency, description=t.description, ts=t.ts) for t in txs]}
    finally:
        db.close()
