"""Database Operations"""

from app import models, schemas
import uuid
import secrets
from sqlmodel import Session


def get_account(db: Session, account_id: str):
    """Retrieve an account by account_id"""
    return (
        db.query(models.Account).filter(models.Account.account_id == account_id).first()
    )


def get_destination(db: Session, destination_id: str):
    """Retrieve a destination by destination_id"""
    return (
        db.query(models.Destination)
        .filter(models.Destination.id == destination_id)
        .first()
    )


def get_account_by_email(db: Session, email: str):
    """Retrieve an account by email address"""
    return db.query(models.Account).filter(models.Account.email == email).first()


def create_account(db: Session, account: schemas.AccountCreate):
    """Create a new account in the database."""
    db_account = models.Account(
        email=account.email,
        account_id=str(uuid.uuid4()),  # Generate a new UUID for account_id
        name=account.name,
        app_secret_token=secrets.token_hex(
            16
        ),  # Generate a secure token for app_secret_token
        website=account.website,
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def delete_account(db: Session, account_id: str):
    """Delete an account by account_id"""
    db_account = get_account(db, account_id)
    if db_account:
        db.delete(db_account)
        db.commit()
    return db_account


def get_destinations_by_account(db: Session, account_id: str):
    """Retrieve all destinations associated with an account"""
    return (
        db.query(models.Destination)
        .filter(models.Destination.account_id == account_id)
        .all()
    )


def create_destination(
    db: Session, destination: schemas.DestinationCreate, account_id: str
):
    """Create a new destination for an account"""
    db_destination = models.Destination(
        url=destination.url,
        http_method=destination.http_method,
        headers=destination.headers,  # Assuming headers is a dictionary
        account_id=account_id,
    )
    db.add(db_destination)
    db.commit()
    db.refresh(db_destination)
    return db_destination


def delete_destination(db: Session, destination_id: str):
    """Delete a destination by destination_id"""
    db_destination = (
        db.query(models.Destination)
        .filter(models.Destination.id == destination_id)
        .first()
    )
    if db_destination:
        db.delete(db_destination)
        db.commit()
    return db_destination


def get_account_by_secret_token(db: Session, token: str):
    """Retrieve an account by app_secret_token"""
    return (
        db.query(models.Account)
        .filter(models.Account.app_secret_token == token)
        .first()
    )
