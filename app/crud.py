from sqlalchemy.orm import Session
from . import models, auth
import time

# Users
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, email: str, password: str):
    hashed = auth.get_password_hash(password)
    user = models.User(email=email, hashed_password=hashed)
    db.add(user); db.commit(); db.refresh(user); return user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user: return None
    if not auth.verify_password(password, user.hashed_password): return None
    return user

# Accounts
def create_account(db: Session, user_id: int, account_in):
    acc = models.Account(user_id=user_id, name=account_in.name, platform=account_in.platform or '', type=account_in.type or '', manual_balance=account_in.manual_balance or 0.0, manual_override=account_in.manual_override if account_in.manual_override is not None else True, currency=account_in.currency or 'USD', update_mode=account_in.update_mode or 'manual', notes=account_in.notes)
    db.add(acc); db.commit(); db.refresh(acc); return acc

def list_accounts(db: Session, user_id: int):
    return db.query(models.Account).filter(models.Account.user_id == user_id).all()

def get_account(db: Session, user_id: int, account_id: int):
    return db.query(models.Account).filter(models.Account.user_id == user_id, models.Account.id == account_id).first()

# Transactions
def create_transaction(db: Session, user_id: int, tx_in):
    tx = models.Transaction(user_id=user_id, account_id=tx_in.account_id, tx_type=tx_in.tx_type, amount=tx_in.amount, currency=tx_in.currency or 'USD', description=tx_in.description, ts=tx_in.ts)
    db.add(tx); db.commit(); db.refresh(tx); return tx

def list_transactions(db: Session, user_id: int, account_id: int = None):
    q = db.query(models.Transaction).filter(models.Transaction.user_id == user_id)
    if account_id:
        q = q.filter(models.Transaction.account_id == account_id)
    return q.order_by(models.Transaction.ts.desc()).all()

# Sync helpers (simple)
def upsert_accounts(db: Session, user_id: int, accounts_data: list):
    out = []
    for a in accounts_data:
        if 'id' in a and a['id']:
            acc = get_account(db, user_id, a['id'])
            if acc:
                for k,v in a.items():
                    if hasattr(acc, k) and k != 'id': setattr(acc, k, v)
                db.add(acc); db.commit(); db.refresh(acc); out.append(acc)
                continue
        # create
        from .schemas import AccountCreate
        ac = AccountCreate(**a)
        acc = create_account(db, user_id, ac)
        out.append(acc)
    return out

def upsert_transactions(db: Session, user_id: int, txs: list):
    out = []
    for t in txs:
        # simple create - in production prefer dedup by uuid
        from .schemas import TransactionCreate
        tc = TransactionCreate(**t)
        tx = create_transaction(db, user_id, tc)
        out.append(tx)
    return out
