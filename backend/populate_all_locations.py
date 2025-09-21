#!/usr/bin/env python3
"""
Script to populate all location tables by calling the stations endpoint multiple times
"""

import requests
import time
from database import AirQualityDatabase

def populate_all_locations():
    """Call the stations endpoint multiple times to populate all location tables"""
    print("🚀 Populating all location tables via stations endpoint...")
    
    db = AirQualityDatabase()
    base_url = "http://localhost:5000"
    
    total_calls = 0
    successful_calls = 0
    
    try:
        # Call the stations endpoint 20 times to populate all locations
        print(f"\n📡 Calling /api/aqi/nyc/stations endpoint 20 times...")
        
        for i in range(20):
            try:
                response = requests.get(f"{base_url}/api/aqi/nyc/stations")
                
                if response.status_code == 200:
                    data = response.json()
                    stations_count = len(data.get('stations', []))
                    print(f"   ✅ Call {i+1}/20 successful ({stations_count} stations)")
                    successful_calls += 1
                else:
                    print(f"   ❌ Call {i+1}/20 failed: {response.status_code}")
                
                total_calls += 1
                
                # Wait 1 second between calls
                time.sleep(1)
                
            except requests.exceptions.ConnectionError:
                print(f"   ❌ Call {i+1}/20 failed: Cannot connect to backend")
                total_calls += 1
            except Exception as e:
                print(f"   ❌ Call {i+1}/20 failed: {e}")
                total_calls += 1
        
        # Also call the current endpoint a few times for home location
        print(f"\n📡 Calling /api/aqi/nyc/current endpoint 5 times for home location...")
        
        for i in range(5):
            try:
                response = requests.get(f"{base_url}/api/aqi/nyc/current")
                
                if response.status_code == 200:
                    print(f"   ✅ Current AQI call {i+1}/5 successful")
                    successful_calls += 1
                else:
                    print(f"   ❌ Current AQI call {i+1}/5 failed")
                
                total_calls += 1
                time.sleep(1)
                
            except Exception as e:
                print(f"   ❌ Current AQI call {i+1}/5 failed: {e}")
                total_calls += 1
        
        print(f"\n📊 API Call Summary:")
        print(f"   Total calls made: {total_calls}")
        print(f"   Successful calls: {successful_calls}")
        print(f"   Failed calls: {total_calls - successful_calls}")
        
        # Show final database stats
        print(f"\n📊 Final Database Statistics:")
        stats = db.get_database_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        # Test the location endpoints now that they should have data
        print(f"\n🧪 Testing location endpoints...")
        locations = ["home", "work", "football", "studio", "daycare"]
        
        for location in locations:
            try:
                response = requests.get(f"{base_url}/api/location/{location}/current")
                if response.status_code == 200:
                    data = response.json()
                    aqi = data.get('aqi_value', 'N/A')
                    print(f"   ✅ {location}: AQI {aqi}")
                else:
                    print(f"   ❌ {location}: {response.status_code}")
            except Exception as e:
                print(f"   ❌ {location}: {e}")
        
        print(f"\n🎉 Database population complete!")
        
    except Exception as e:
        print(f"❌ Error during population: {e}")

if __name__ == "__main__":
    populate_all_locations()
