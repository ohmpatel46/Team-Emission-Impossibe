#!/usr/bin/env python3
"""
Database population script for AirWatch
Populate the database with initial demo data
"""

import requests
import time
from database import AirQualityDatabase

def populate_database():
    """Populate database with initial data"""
    print("🌱 Populating AirWatch Database...")
    
    db = AirQualityDatabase()
    
    # Make API calls to populate data
    base_url = "http://localhost:5000"
    
    try:
        print("📡 Fetching current NYC air quality data...")
        response = requests.get(f"{base_url}/api/aqi/nyc/current")
        if response.status_code == 200:
            print("✅ Current AQI data fetched and saved")
        else:
            print("❌ Failed to fetch current AQI data")
        
        print("📡 Fetching NYC stations data...")
        response = requests.get(f"{base_url}/api/aqi/nyc/stations")
        if response.status_code == 200:
            print("✅ Stations data fetched and saved")
        else:
            print("❌ Failed to fetch stations data")
        
        # Add some historical data by making multiple calls
        print("📈 Adding historical data (5 calls)...")
        for i in range(5):
            requests.get(f"{base_url}/api/aqi/nyc/current")
            requests.get(f"{base_url}/api/aqi/nyc/stations")
            time.sleep(1)  # Wait 1 second between calls
        
        print("✅ Historical data added")
        
        # Add a sample user profile
        print("👤 Adding sample user profile...")
        sample_profile = {
            "userId": "demo_user_123",
            "age": 28,
            "sex": "female",
            "smoking_status": "never",
            "health_conditions": ["asthma"]
        }
        
        success = db.save_user_profile("demo_user_123", sample_profile)
        if success:
            print("✅ Sample user profile added")
        else:
            print("❌ Failed to add sample user profile")
        
        # Show final stats
        stats = db.get_database_stats()
        print(f"\n📊 Final Database Statistics:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        print(f"\n🎉 Database population complete!")
        print(f"💡 Use 'python view_database.py' to view the data")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
        print("💡 Make sure to start the backend first: python app.py")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    populate_database()
