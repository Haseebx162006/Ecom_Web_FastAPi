-- Migration script to add new columns to products table
-- Run this directly on your PostgreSQL database if the automatic migration doesn't work

-- Add featured column if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='products' AND column_name='featured'
    ) THEN
        ALTER TABLE products ADD COLUMN featured BOOLEAN DEFAULT FALSE;
        RAISE NOTICE 'Added featured column';
    ELSE
        RAISE NOTICE 'featured column already exists';
    END IF;
END $$;

-- Add image_url column if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name='products' AND column_name='image_url'
    ) THEN
        ALTER TABLE products ADD COLUMN image_url VARCHAR(500);
        RAISE NOTICE 'Added image_url column';
    ELSE
        RAISE NOTICE 'image_url column already exists';
    END IF;
END $$;

