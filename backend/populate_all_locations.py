#!/usr/bin/env python3
"""
Populate All Locations Script
Populate the database with sample data for all 5 locations
"""

import requests
import json
import time
import random

# Backend API base URL
BASE_URL = "http://localhost:5000"

# Location mapping
LOCATIONS = {
    'home': 'Manhattan Midtown',
    'work': 'Brooklyn Downtown', 
    'football': 'Queens Astoria',
    'studio': 'Bronx South',
    'daycare': 'Staten Island North'
}

def populate_location_data(location_id, location_name, num_records=10):
    """Populate data for a specific location"""
    print(f"🏠 Populating {location_name} ({location_id}) with {num_records} records...")
    
    success_count = 0
    for i in range(num_records):
        try:
            # Call the location-specific current endpoint
            response = requests.get(f"{BASE_URL}/api/location/{location_id}/current")
            
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ Record {i+1}: AQI {data.get('aqi_value', 'N/A')}")
                success_count += 1
            else:
                print(f"  ❌ Record {i+1}: HTTP {response.status_code}")
            
            # Small delay between requests
            time.sleep(0.5)
            
        except Exception as e:
            print(f"  ❌ Record {i+1}: Error - {e}")
    
    print(f"📊 {location_name}: {success_count}/{num_records} records successful")
    return success_count

def populate_all_locations():
    """Populate data for all locations"""
    print("🚀 Starting population of all locations...")
    print("=" * 50)
    
    total_success = 0
    total_records = 0
    
    for location_id, location_name in LOCATIONS.items():
        records_per_location = random.randint(8, 12)  # Random between 8-12 records
        success = populate_location_data(location_id, location_name, records_per_location)
        
        total_success += success
        total_records += records_per_location
        
        print()  # Empty line for readability
    
    print("=" * 50)
    print(f"🎯 Population Summary:")
    print(f"   Total Records Attempted: {total_records}")
    print(f"   Total Records Successful: {total_success}")
    print(f"   Success Rate: {(total_success/total_records)*100:.1f}%")
    
    if total_success > 0:
        print("✅ Population completed successfully!")
    else:
        print("❌ Population failed - check if backend server is running")

if __name__ == "__main__":
    print("🔧 Make sure the Flask backend server is running on http://localhost:5000")
    print("   Run: python app.py")
    print()
    
    try:
        # Test if backend is running
        response = requests.get(f"{BASE_URL}/api/aqi/nyc/current", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running!")
            populate_all_locations()
        else:
            print("❌ Backend server is not responding properly")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server!")
        print("   Please start the Flask server first: python app.py")
    except Exception as e:
        print(f"❌ Error: {e}")
