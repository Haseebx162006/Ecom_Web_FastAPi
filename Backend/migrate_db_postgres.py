"""
Migration script to add new columns to existing PostgreSQL database tables.
Run this once to update your database schema.
"""
from sqlalchemy import create_engine, text
from database import engine
import os
from dotenv import load_dotenv

load_dotenv()

def migrate_database():
    """Add missing columns to existing tables"""
    try:
        with engine.connect() as conn:
            # Check if columns exist
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='products' AND column_name IN ('featured', 'image_url')
            """)
            result = conn.execute(check_query)
            existing_columns = [row[0] for row in result]
            
            if 'featured' not in existing_columns:
                print("Adding 'featured' column to products table...")
                conn.execute(text("ALTER TABLE products ADD COLUMN featured BOOLEAN DEFAULT FALSE"))
                conn.commit()
                print("✓ Added 'featured' column")
            else:
                print("✓ 'featured' column already exists")
            
            if 'image_url' not in existing_columns:
                print("Adding 'image_url' column to products table...")
                conn.execute(text("ALTER TABLE products ADD COLUMN image_url VARCHAR(500)"))
                conn.commit()
                print("✓ Added 'image_url' column")
            else:
                print("✓ 'image_url' column already exists")
                
    except Exception as e:
        print(f"Error during migration: {e}")
        import traceback
        traceback.print_exc()
        # Try to rollback if possible
        try:
            conn.rollback()
        except:
            pass
        raise

if __name__ == "__main__":
    print("Starting database migration for PostgreSQL...")
    migrate_database()
    print("Migration completed!")

