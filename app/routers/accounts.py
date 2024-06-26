"""Accounts"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from app.database import get_session
from pydantic import BaseModel, EmailStr
from typing import Optional

router = APIRouter()


class CreateAccountPayload(BaseModel):
    """Payload to create account"""

    email: EmailStr
    name: str
    website: Optional[str] = None


@router.post("/")
def create_account(
    account: CreateAccountPayload,
    session: Session = Depends(get_session),
):
    """Create account"""

    # Get account by email and Check if the user already registered
    db_account = crud.get_account_by_email(session, email=account.email)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create account
    return crud.create_account(db=session, account=account)


@router.get("/{account_id}")
def get_account(account_id: str, db: Session = Depends(get_session)):
    """Get account"""

    # Get account by id
    db_account = crud.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    return db_account


@router.delete("/{account_id}")
def delete_account(account_id: str, db: Session = Depends(get_session)):
    """Delete Account"""

    db_account = crud.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    return crud.delete_account(db=db, account_id=account_id)
