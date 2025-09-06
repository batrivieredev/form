import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import sys
from alembic import command
from alembic.config import Config

# Load environment variables
load_dotenv()

# Database connection parameters
DB_NAME = "form_db"
DB_USER = "batrivieredev"
DB_PASSWORD = ""  # No password needed for local development
DB_HOST = "localhost"

def create_database():
    """Create the database if it doesn't exist."""
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            user=DB_USER,
            host=DB_HOST,
            database="postgres"  # Connect to default database first
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (DB_NAME,))
        exists = cursor.fetchone()

        if not exists:
            print(f"Creating database {DB_NAME}...")
            cursor.execute(f'CREATE DATABASE {DB_NAME}')
            print("Database created successfully!")
        else:
            print(f"Database {DB_NAME} already exists.")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def setup_database():
    """Set up the database schema and apply migrations."""
    try:
        # Run database migrations
        print("Applying database migrations...")
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        print("Migrations applied successfully!")

        # Set up cleanup functionality
        print("Setting up user cleanup functionality...")
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            host=DB_HOST
        )
        cursor = conn.cursor()

        # Create cleanup function directly
        cleanup_function = """
        CREATE OR REPLACE FUNCTION cleanup_inactive_users()
        RETURNS INTEGER AS
        $$
        DECLARE
            count INTEGER;
        BEGIN
            UPDATE users
            SET is_active = false
            WHERE is_active = true
            AND last_login < CURRENT_TIMESTAMP - INTERVAL '1 year';
            GET DIAGNOSTICS count = ROW_COUNT;
            RETURN count;
        END;
        $$ LANGUAGE plpgsql;
        """
        cursor.execute(cleanup_function)
        conn.commit()
        cursor.close()
        conn.close()
        print("Cleanup functionality configured successfully!")
        return True

    except Exception as e:
        print(f"Error setting up database: {e}")
        return False

if __name__ == "__main__":
    print("Starting database setup...")

    if not create_database():
        print("Failed to create database. Exiting.")
        sys.exit(1)

    if not setup_database():
        print("Failed to set up database. Exiting.")
        sys.exit(1)

    print("Database setup completed successfully!")
