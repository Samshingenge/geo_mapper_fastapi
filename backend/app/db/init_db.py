import logging
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from geoalchemy2.functions import AddGeometryColumn, DropGeometryColumn

from app.db.base import engine, Base
from app.models.region import Region

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db() -> None:
    """
    Initialize the database by creating all tables.
    """
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")
        
        # Enable PostGIS extension if it doesn't exist
        with engine.connect() as conn:
            # Enable PostGIS extension
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
            conn.commit()
            logger.info("PostGIS extension enabled.")
            
    except SQLAlchemyError as e:
        logger.error(f"Error initializing database: {e}")
        raise

def drop_tables() -> None:
    """
    Drop all tables in the database.
    """
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("All tables dropped successfully.")
    except SQLAlchemyError as e:
        logger.error(f"Error dropping tables: {e}")
        raise

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialization complete.")
