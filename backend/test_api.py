#!/usr/bin/env python3
"""
Test script for AirWatch Python Backend API
Tests all endpoints and displays responses
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"
ENDPOINTS = {
    "health": "/health",
    "current_aqi": "/api/aqi/nyc/current", 
    "stations": "/api/aqi/nyc/stations",
    "user_profile": "/api/users/profile",
    "health_risk": "/api/users/profile/test_user/health-risk"
}

def test_endpoint(method, endpoint, data=None):
    """Test a single endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        print(f"✅ {method} {endpoint}")
        print(f"   Status: {response.status_code}")
        print(f"   Response:")
        print(json.dumps(response.json(), indent=2))
        print("-" * 50)
        
        return response.json()
        
    except requests.exceptions.ConnectionError:
        print(f"❌ {method} {endpoint}")
        print(f"   Error: Cannot connect to server at {BASE_URL}")
        print(f"   Make sure the Python backend is running!")
        print("-" * 50)
        return None
        
    except Exception as e:
        print(f"❌ {method} {endpoint}")
        print(f"   Error: {str(e)}")
        print("-" * 50)
        return None

def main():
    """Run all API tests"""
    print("🧪 Testing AirWatch Python Backend API")
    print(f"🌐 Base URL: {BASE_URL}")
    print(f"⏰ Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Test health check
    print("\n🏥 Testing Health Check...")
    test_endpoint("GET", ENDPOINTS["health"])
    
    # Test current AQI endpoint
    print("\n🌍 Testing Current NYC Air Quality...")
    current_data = test_endpoint("GET", ENDPOINTS["current_aqi"])
    
    if current_data:
        print(f"   📊 Current AQI: {current_data['current']['aqi_value']} ({current_data['current']['aqi_category']})")
        print(f"   📍 Location: {current_data['current']['location']}")
        print(f"   🕐 Last Update: {current_data['current']['reading_time']}")
        print(f"   📈 Historical Points: {len(current_data['historical'])}")
    
    # Test stations endpoint
    print("\n🏢 Testing NYC Monitoring Stations...")
    stations_data = test_endpoint("GET", ENDPOINTS["stations"])
    
    if stations_data:
        print(f"   📍 Total Stations: {len(stations_data['stations'])}")
        for station in stations_data['stations']:
            print(f"   - {station['location']}: AQI {station['aqi_value']} ({station['aqi_category']})")
    
    # Test user profile creation
    print("\n👤 Testing User Profile Creation...")
    profile_data = {
        "userId": "test_user_123",
        "age": 28,
        "sex": "female",
        "smoking_status": "never",
        "health_conditions": ["asthma"]
    }
    test_endpoint("POST", ENDPOINTS["user_profile"], profile_data)
    
    # Test health risk assessment
    print("\n⚠️ Testing Health Risk Assessment...")
    test_endpoint("GET", ENDPOINTS["health_risk"])
    
    print("\n🎉 API Testing Complete!")
    print("\n💡 Next Steps:")
    print("   1. Make sure your frontend is configured to use port 5000")
    print("   2. Update frontend BACKEND_CONFIG.baseUrl to 'http://localhost:5000'")
    print("   3. Test the frontend integration")

if __name__ == "__main__":
    main()
