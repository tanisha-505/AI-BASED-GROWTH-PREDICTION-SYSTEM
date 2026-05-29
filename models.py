# models.py
# Two sections:
#   1. SQLAlchemy ORM models  → define MySQL tables
#   2. Pydantic schemas       → validate API request/response data

from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import datetime
from database import Base


# ─────────────────────────────────────────
# SECTION 1 — SQLAlchemy ORM (MySQL tables)
# ─────────────────────────────────────────

class SalesData(Base):
    """Maps to the `sales_data` table in MySQL."""
    __tablename__ = "sales_data"

    id                = Column(Integer, primary_key=True, index=True, autoincrement=True)
    month             = Column(Integer, nullable=False)
    year              = Column(Integer, nullable=False)
    sales             = Column(Float, nullable=False)
    marketing_spend   = Column(Float, nullable=False)
    num_employees     = Column(Integer, nullable=False)
    region            = Column(String(50), nullable=False)
    product_category  = Column(String(100), nullable=False)
    created_at        = Column(DateTime, server_default=func.now())


class Prediction(Base):
    """Maps to the `predictions` table in MySQL."""
    __tablename__ = "predictions"

    id               = Column(Integer, primary_key=True, index=True, autoincrement=True)
    predicted_sales  = Column(Float)
    model_used       = Column(String(100))
    month            = Column(Integer)
    year             = Column(Integer)
    marketing_spend  = Column(Float)
    num_employees    = Column(Integer)
    region           = Column(String(50))
    product_category = Column(String(100))
    timestamp        = Column(String(50))
    created_at       = Column(DateTime, server_default=func.now())


    
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(200), nullable=False)

    

# ─────────────────────────────────────────
# SECTION 2 — Pydantic Schemas (API validation)
# ─────────────────────────────────────────

class SalesRecordSchema(BaseModel):
    """Schema for a single sales record (used in manual insert)."""
    month: int
    year: int
    sales: float
    marketing_spend: float
    num_employees: int
    region: str
    product_category: str


class PredictRequest(BaseModel):
    """Input features sent by the user to get a prediction."""
    month: int
    year: int
    marketing_spend: float
    num_employees: int
    region: str
    product_category: str


class PredictResponse(BaseModel):
    """Response returned after a prediction is made."""
    predicted_sales: float
    model_used: str = "Linear Regression"
    input_features: dict
    timestamp: str

    # class User(Base):
    # __tablename__ = "users"

    # id = Column(Integer, primary_key=True)
    # name = Column(String(100))
    # email = Column(String(100), unique=True)
    # password = Column(String(200))


  
from pydantic import BaseModel

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str