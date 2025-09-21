#!/usr/bin/env python3
"""
Database viewer script for AirWatch
View air quality data stored in SQLite database
"""

import sqlite3
import json
from datetime import datetime
from database import AirQualityDatabase, LOCATION_MAPPING

def view_database():
    """View database contents"""
    db = AirQualityDatabase()
    
    print("🗄️ AirWatch Database Viewer")
    print("=" * 50)
    
    # Get database stats
    stats = db.get_database_stats()
    print("\n📊 Database Statistics:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print(f"\n📍 Location Mapping:")
    for location, station in LOCATION_MAPPING.items():
        print(f"   {location.title()} → {station.replace('_', ' ').title()}")
    
    # View recent data for each location
    print(f"\n🌬️ Recent Air Quality Data:")
    print("-" * 50)
    
    for location_id in LOCATION_MAPPING.keys():
        print(f"\n🏠 {location_id.title()}:")
        data = db.get_latest_location_data(location_id)
        
        if data:
            print(f"   AQI: {data['aqi_value']} ({data['aqi_category']})")
            print(f"   Primary Pollutant: {data['primary_pollutant']}")
            print(f"   PM2.5: {data['pm25']} μg/m³")
            print(f"   PM10: {data['pm10']} μg/m³")
            print(f"   Temperature: {data['temperature']}°C")
            print(f"   Humidity: {data['humidity']}%")
            print(f"   Last Updated: {data['reading_time']}")
        else:
            print("   No data available")
    
    # View NYC stations data
    print(f"\n🏢 NYC Monitoring Stations:")
    print("-" * 50)
    
    stations_data = db.get_all_stations_data()
    if stations_data:
        for station in stations_data[:5]:  # Show first 5 stations
            print(f"\n📍 {station['location']}:")
            print(f"   AQI: {station['aqi_value']} ({station['aqi_category']})")
            print(f"   PM2.5: {station['pm25']} μg/m³")
            print(f"   Last Updated: {station['reading_time']}")
    else:
        print("   No station data available")
    
    # View user profiles
    print(f"\n👤 User Profiles:")
    print("-" * 50)
    
    conn = sqlite3.connect("air_quality.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, age, sex, smoking_status, health_conditions FROM user_profiles")
    profiles = cursor.fetchall()
    conn.close()
    
    if profiles:
        for profile in profiles:
            user_id, age, sex, smoking_status, health_conditions = profile
            health_conditions = json.loads(health_conditions) if health_conditions else []
            print(f"\n👤 User: {user_id}")
            print(f"   Age: {age}")
            print(f"   Sex: {sex}")
            print(f"   Smoking Status: {smoking_status}")
            print(f"   Health Conditions: {', '.join(health_conditions) if health_conditions else 'None'}")
    else:
        print("   No user profiles found")

def view_location_history(location_id, hours=24):
    """View historical data for a specific location"""
    if location_id not in LOCATION_MAPPING:
        print(f"❌ Invalid location: {location_id}")
        print(f"Valid locations: {', '.join(LOCATION_MAPPING.keys())}")
        return
    
    db = AirQualityDatabase()
    data = db.get_location_history(location_id, hours)
    
    print(f"\n📈 {location_id.title()} - Last {hours} Hours:")
    print("-" * 50)
    
    if data:
        for record in data[:10]:  # Show first 10 records
            timestamp = record['timestamp']
            aqi = record['aqi_value']
            category = record['aqi_category']
            print(f"   {timestamp}: AQI {aqi} ({category})")
    else:
        print("   No historical data available")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        location = sys.argv[1]
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        view_location_history(location, hours)
    else:
        view_database()
        
    print(f"\n💡 Usage:")
    print(f"   python view_database.py                    # View all data")
    print(f"   python view_database.py home               # View home history")
    print(f"   python view_database.py work 48            # View work history (48 hours)")
