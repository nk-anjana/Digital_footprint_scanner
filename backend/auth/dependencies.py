from fastapi import Request, HTTPException, status
from jose import jwt, JWTError

from backend.config import SECRET_KEY, ALGORITHM


def get_current_user(request: Request) -> str:
    """
    Extracts and validates JWT from Authorization header.
    Expects: Authorization: Bearer <token>
    """

    # Get Authorization header
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    #Extract token
    token = auth_header.split(" ")[1]

    try:
        #Decode JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        #Extract values
        username = payload.get("sub")
        token_type = payload.get("type")

        #Validate token contents
        if username is None or token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )

        return username

    except JWTError:
        # Covers expired, invalid signature, malformed token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )