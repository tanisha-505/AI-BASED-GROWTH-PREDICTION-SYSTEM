# database.py
# MySQL connection using SQLAlchemy + mysql-connector-python

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# -----------------------------------------------
# CHANGE these values to match your MySQL setup
DB_USER     = "root"
DB_PASSWORD = "1410"   # password you set during MySQL install
DB_HOST     = "localhost"
DB_PORT     = "3306"
DB_NAME     = "growth_prediction_db"
# -----------------------------------------------

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency: provides a database session to each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection():
    """Test if MySQL is reachable. Called on server startup."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Connected to MySQL successfully!")
    except Exception as e:
        print(f"❌ MySQL connection failed: {e}")
        raise