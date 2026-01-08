"""
Migration script to add new columns to existing database tables.
Run this once to update your database schema.
"""
from sqlalchemy import text
from database import engine

def migrate_database():
    """Add missing columns to existing tables"""
    with engine.connect() as conn:
        # Check if featured column exists in products table
        try:
            # For SQLite
            result = conn.execute(text("PRAGMA table_info(products)"))
            columns = [row[1] for row in result]
            
            if 'featured' not in columns:
                print("Adding 'featured' column to products table...")
                conn.execute(text("ALTER TABLE products ADD COLUMN featured BOOLEAN DEFAULT 0"))
                conn.commit()
                print("✓ Added 'featured' column")
            else:
                print("✓ 'featured' column already exists")
            
            if 'image_url' not in columns:
                print("Adding 'image_url' column to products table...")
                conn.execute(text("ALTER TABLE products ADD COLUMN image_url VARCHAR(500)"))
                conn.commit()
                print("✓ Added 'image_url' column")
            else:
                print("✓ 'image_url' column already exists")
                
        except Exception as e:
            print(f"Error during migration: {e}")
            # Try to rollback if possible
            try:
                conn.rollback()
            except:
                pass
            raise

if __name__ == "__main__":
    print("Starting database migration...")
    migrate_database()
    print("Migration completed!")

