#!/usr/bin/env python3
"""
Script to fix database schema by adding missing columns
"""

import sqlite3

def fix_database_schema():
    """Add missing columns to database tables"""
    print("🔧 Fixing database schema...")
    
    try:
        conn = sqlite3.connect('air_quality.db')
        cursor = conn.cursor()
        
        # Add missing columns to nyc_stations table
        print("📋 Adding missing columns to nyc_stations table...")
        
        # Check if columns exist first
        cursor.execute("PRAGMA table_info(nyc_stations)")
        columns = [col[1] for col in cursor.fetchall()]
        print(f"Current columns: {columns}")
        
        # Add missing columns
        missing_columns = [
            ("so2", "REAL"),
            ("co", "REAL"),
            ("temperature", "REAL"),
            ("humidity", "REAL")
        ]
        
        for col_name, col_type in missing_columns:
            if col_name not in columns:
                try:
                    cursor.execute(f"ALTER TABLE nyc_stations ADD COLUMN {col_name} {col_type}")
                    print(f"   ✅ Added column: {col_name}")
                except sqlite3.OperationalError as e:
                    print(f"   ❌ Failed to add {col_name}: {e}")
            else:
                print(f"   ⚠️  Column {col_name} already exists")
        
        conn.commit()
        conn.close()
        
        print("✅ Database schema fixed!")
        
    except Exception as e:
        print(f"❌ Error fixing schema: {e}")

if __name__ == "__main__":
    fix_database_schema()
