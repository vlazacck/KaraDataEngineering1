from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError  # Add this import
from sqlalchemy.ext.declarative import declarative_base
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Database URL (PostgreSQL)
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/ethiopian_medical_data"

# Create engine
engine = create_engine(DATABASE_URL)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        logging.info("Database connection established.")
        yield db
    except SQLAlchemyError as e:  # Use the imported exception
        logging.error(f"Database error: {e}")
        raise
    finally:
        db.close()
        logging.info("Database connection closed.")