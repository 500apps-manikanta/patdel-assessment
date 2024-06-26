"""Destinations"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from app.database import get_session
from pydantic import BaseModel

router = APIRouter()


class CreateDestinationPayload(BaseModel):
    """Payload to create destination"""

    url: str
    http_method: str
    headers: dict


@router.post("/{account_id}")
def create_destination(
    account_id: str,
    destination: CreateDestinationPayload,
    db: Session = Depends(get_session),
):
    """Create destination"""

    # Retrieve account from database based on account_id
    db_account = crud.get_account(db, account_id=account_id)

    # If account does not exist, raise HTTP 404 Not Found exception
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    # Create a new destination associated with the account in the database
    return crud.create_destination(
        db=db, destination=destination, account_id=account_id
    )


@router.get("/{account_id}")
def get_destinations(account_id: str, db: Session = Depends(get_session)):
    """Get destinations based on Account id"""

    # Retrieve account from database based on account_id
    db_account = crud.get_account(db, account_id=account_id)

    # If account does not exist, raise HTTP 404 Not Found exception
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    # Retrieve all destinations associated with the account from the database
    return crud.get_destinations_by_account(db=db, account_id=account_id)


@router.delete("/{destination_id}")
def delete_destination(destination_id: str, db: Session = Depends(get_session)):
    """Delete destination"""

    # Retrieve destination from database based on destination_id
    db_destination = crud.get_destination(db, destination_id=destination_id)

    # If destination does not exist, raise HTTP 404 Not Found exception
    if db_destination is None:
        raise HTTPException(status_code=404, detail="Destination not found")

    # Delete the destination from the database
    return crud.delete_destination(db=db, destination_id=destination_id)
