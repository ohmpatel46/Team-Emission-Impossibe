#!/usr/bin/env python3
"""
Temporary script to call each station through the API 10 times
and populate the database with response data
"""

import requests
import time
from database import AirQualityDatabase

def populate_stations_from_api():
    """Call each station API endpoint 10 times and save data"""
    print("🚀 Populating database with API calls to each station...")
    
    db = AirQualityDatabase()
    base_url = "http://localhost:5000"
    
    # User location endpoints (these map to stations internally)
    locations = [
        "home",      # maps to manhattan_midtown
        "work",      # maps to brooklyn_downtown
        "football",  # maps to queens_astoria
        "studio",    # maps to bronx_south
        "daycare"    # maps to staten_island_north
    ]
    
    total_calls = 0
    successful_calls = 0
    
    try:
        for location in locations:
            print(f"\n📡 Calling API for {location}...")
            
            for i in range(10):
                try:
                    # Call the location-specific endpoint
                    response = requests.get(f"{base_url}/api/location/{location}/current")
                    
                    if response.status_code == 200:
                        data = response.json()
                        print(f"   ✅ Call {i+1}/10 successful")
                        successful_calls += 1
                    else:
                        print(f"   ❌ Call {i+1}/10 failed: {response.status_code}")
                    
                    total_calls += 1
                    
                    # Wait 1 second between calls
                    time.sleep(1)
                    
                except requests.exceptions.ConnectionError:
                    print(f"   ❌ Call {i+1}/10 failed: Cannot connect to backend")
                    total_calls += 1
                except Exception as e:
                    print(f"   ❌ Call {i+1}/10 failed: {e}")
                    total_calls += 1
        
        print(f"\n📊 API Call Summary:")
        print(f"   Total calls made: {total_calls}")
        print(f"   Successful calls: {successful_calls}")
        print(f"   Failed calls: {total_calls - successful_calls}")
        
        # Also make some calls to the general endpoints
        print(f"\n📡 Making additional calls to general endpoints...")
        
        for i in range(5):
            try:
                # Call current AQI endpoint
                response = requests.get(f"{base_url}/api/aqi/nyc/current")
                if response.status_code == 200:
                    print(f"   ✅ Current AQI call {i+1}/5 successful")
                else:
                    print(f"   ❌ Current AQI call {i+1}/5 failed")
                
                # Call stations endpoint
                response = requests.get(f"{base_url}/api/aqi/nyc/stations")
                if response.status_code == 200:
                    print(f"   ✅ Stations call {i+1}/5 successful")
                else:
                    print(f"   ❌ Stations call {i+1}/5 failed")
                
                time.sleep(1)
                
            except Exception as e:
                print(f"   ❌ General call {i+1}/5 failed: {e}")
        
        # Show final database stats
        print(f"\n📊 Final Database Statistics:")
        stats = db.get_database_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")
        
        print(f"\n🎉 Database population complete!")
        
    except Exception as e:
        print(f"❌ Error during population: {e}")

if __name__ == "__main__":
    populate_stations_from_api()
