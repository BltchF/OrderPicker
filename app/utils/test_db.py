import os
from dotenv import load_dotenv
import sqlalchemy  # Or your preferred database library for PostgreSQL
from sqlalchemy import text, create_engine

# Load environment variables from ../../../.env
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
dotenv_path = os.path.join(project_root, '.env') 
load_dotenv(dotenv_path)

local_test_database_url = os.getenv('LOCAL_TEST_DATABASE_URL').replace("://", "ql://", 1)

def get_database_engine():
    """Creates a database engine and tests the connection."""
    try:
        engine = create_engine(local_test_database_url)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("Database connection successful!")
        return engine
    except sqlalchemy.exc.OperationalError as e:
        print(f"Database connection failed: {e}")
        return None  # Or raise an exception if you prefer

