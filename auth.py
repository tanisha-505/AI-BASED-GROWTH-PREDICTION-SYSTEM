# auth.py — NEW FILE
# ✅ Password hashing using bcrypt
# ✅ JWT token creation and verification

from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, status

# ── Password Hashing ──────────────────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Convert plain password to hashed password."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if plain password matches hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


# ── JWT Token ─────────────────────────────────────────────────────────────
SECRET_KEY  = "tanisha_growth_prediction_secret_2024"  # Change in production!
ALGORITHM   = "HS256"
TOKEN_HOURS = 24   # Token valid for 24 hours


def create_token(data: dict) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire    = datetime.utcnow() + timedelta(hours=TOKEN_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email   = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token — no email found"
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is invalid or expired. Please login again."
        )