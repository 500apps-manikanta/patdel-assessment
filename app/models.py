"""Database models"""

from sqlmodel import Column, Field, SQLModel, JSON
from sqlmodel import Field, SQLModel
from typing import Optional
from sqlalchemy import Column, JSON


class Account(SQLModel, table=True):
    """Account Model"""

    __tablename__ = "account"  # Name of the database table

    id: Optional[int] = Field(default=None, primary_key=True)  # Primary key
    email: str = Field(
        max_length=255, unique=True, index=True, nullable=False
    )  # Unique email, indexed
    account_id: str = Field(
        unique=True, index=True, nullable=False
    )  # Unique account ID, indexed
    name: str = Field(nullable=False)  # Account name, not nullable
    app_secret_token: str = Field(
        unique=True, index=True, nullable=False
    )  # Unique secret token, indexed
    website: Optional[str] = Field(default=None, nullable=True)  # Optional website URL


class Destination(SQLModel, table=True):
    """Destination Model"""

    __tablename__ = "destination"  # Name of the database table

    id: Optional[int] = Field(default=None, primary_key=True)  # Primary key
    url: str = Field(nullable=False)  # Destination URL, not nullable
    http_method: str = Field(nullable=False)  # HTTP method (POST, GET), not nullable
    headers: Optional[dict] = Field(
        default=None, sa_column=Column(JSON)
    )  # Optional headers as JSON
    account_id: str = Field(
        nullable=False, max_length=255
    )  # Foreign key to Account table
