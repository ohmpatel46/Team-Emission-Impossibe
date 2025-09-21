#!/usr/bin/env python3
"""
Temporary script to clean all records from the database
"""

import sqlite3

def clean_database():
    """Remove all records from all tables"""
    print("🧹 Cleaning all records from database...")
    
    try:
        # Connect to database
        conn = sqlite3.connect('air_quality.db')
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"📋 Found {len(tables)} tables:")
        for table in tables:
            table_name = table[0]
            print(f"   - {table_name}")
        
        # Delete all records from each table
        total_deleted = 0
        for table in tables:
            table_name = table[0]
            cursor.execute(f"DELETE FROM {table_name}")
            deleted_count = cursor.rowcount
            total_deleted += deleted_count
            print(f"🗑️  Deleted {deleted_count} records from {table_name}")
        
        # Commit changes
        conn.commit()
        conn.close()
        
        print(f"\n✅ Successfully deleted {total_deleted} total records from all tables")
        print("🎉 Database is now clean!")
        
    except Exception as e:
        print(f"❌ Error cleaning database: {e}")

if __name__ == "__main__":
    clean_database()
