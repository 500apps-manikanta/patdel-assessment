"""Webhook"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import httpx
from app import crud
from app.database import get_session

router = APIRouter()


@router.post("/incoming_data")
async def webhook(request: Request, db: Session = Depends(get_session)):
    """Incoming webhook handler"""

    # Extract CL-X-TOKEN from request headers
    cl_x_token = request.headers.get("CL-X-TOKEN")

    # Check if CL-X-TOKEN exists
    if not cl_x_token:
        return {
            "message": "Un Authenticate"
        }  # Return error message if token is missing

    # Retrieve account using the secret token from the database
    account = crud.get_account_by_secret_token(db, cl_x_token)

    # If account not found, raise HTTP 403 Forbidden exception
    if not account:
        raise HTTPException(status_code=403, detail="Invalid Secret Token")

    # Parse incoming JSON data from request
    data = await request.json()

    # Retrieve destinations associated with the account from the database
    destinations = crud.get_destinations_by_account(db, account_id=account.id)

    # Iterate through each destination
    for destination in destinations:
        # Check HTTP method type for each destination
        if destination.http_method.lower() == "get":
            # Perform asynchronous GET request using httpx.AsyncClient
            async with httpx.AsyncClient() as client:
                await client.get(
                    destination.url, params=data, headers=destination.headers
                )
        elif destination.http_method.lower() in ["post", "put"]:
            # Perform asynchronous POST or PUT request using httpx.AsyncClient
            async with httpx.AsyncClient() as client:
                await client.request(
                    method=destination.http_method.upper(),
                    url=destination.url,
                    json=data,
                    headers=destination.headers,
                )

    # Return success message
    return {"message": "Data sent to destinations"}
