#!/usr/bin/env python3
"""
Database Viewer Script
View all tables and data in the air quality database
"""

import sqlite3
import os

def view_database():
    """View all tables and their data in the database"""
    db_path = "air_quality.db"
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("📊 Database Tables:")
        print("=" * 50)
        
        for table in tables:
            table_name = table[0]
            print(f"\n🗂️  Table: {table_name}")
            print("-" * 30)
            
            # Get table schema
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            print("Columns:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"Rows: {count}")
            
            # Show first 5 rows
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
                rows = cursor.fetchall()
                
                print("Sample data (first 5 rows):")
                for i, row in enumerate(rows, 1):
                    print(f"  {i}: {row}")
            
            print()
        
        conn.close()
        print("✅ Database view completed!")
        
    except Exception as e:
        print(f"❌ Error viewing database: {e}")

if __name__ == "__main__":
    view_database()
