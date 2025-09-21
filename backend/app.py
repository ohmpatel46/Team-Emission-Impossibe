from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json
from datetime import datetime, timedelta
import time
import random
from database import AirQualityDatabase, LOCATION_MAPPING, STATION_TO_LOCATION

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Initialize database
db = AirQualityDatabase()

# Configuration
NYC_LAT = 40.7128
NYC_LON = -74.0060

# NYC Monitoring Stations
NYC_STATIONS = [
    {
        "id": "manhattan_midtown",
        "location": "Manhattan Midtown",
        "latitude": 40.7589,
        "longitude": -73.9851
    },
    {
        "id": "brooklyn_downtown", 
        "location": "Brooklyn Downtown",
        "latitude": 40.6943,
        "longitude": -73.9903
    },
    {
        "id": "queens_astoria",
        "location": "Queens Astoria", 
        "latitude": 40.7794,
        "longitude": -73.9217
    },
    {
        "id": "bronx_south",
        "location": "Bronx South",
        "latitude": 40.8448,
        "longitude": -73.8648
    },
    {
        "id": "staten_island_north",
        "location": "Staten Island North",
        "latitude": 40.6415,
        "longitude": -74.0776
    }
]

def get_aqi_category(aqi_value):
    """Convert AQI value to category"""
    if aqi_value <= 50:
        return "good"
    elif aqi_value <= 100:
        return "moderate"
    elif aqi_value <= 150:
        return "unhealthy_sensitive"
    elif aqi_value <= 200:
        return "unhealthy"
    elif aqi_value <= 300:
        return "very_unhealthy"
    else:
        return "hazardous"

def generate_mock_current_data():
    """Generate mock current air quality data"""
    aqi_value = random.randint(40, 120)
    
    return {
        "location": "New York City, NY",
        "aqi_value": aqi_value,
        "aqi_category": get_aqi_category(aqi_value),
        "primary_pollutant": "PM2.5",
        "pm25": round(random.uniform(10, 30), 1),
        "pm10": round(random.uniform(15, 40), 1),
        "o3": round(random.uniform(20, 60), 1),
        "no2": round(random.uniform(10, 35), 1),
        "so2": round(random.uniform(5, 15), 1),
        "co": round(random.uniform(0.5, 2.0), 1),
        "temperature": round(random.uniform(15, 25), 1),
        "humidity": round(random.uniform(50, 80), 1),
        "reading_time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "latitude": NYC_LAT,
        "longitude": NYC_LON
    }

def generate_mock_historical_data():
    """Generate mock historical data for the last 24 hours"""
    historical = []
    now = datetime.now()
    
    for i in range(24):
        time_point = now - timedelta(hours=i)
        aqi_value = random.randint(40, 120)
        
        historical.append({
            "time": time_point.strftime("%H:%M"),
            "aqi": aqi_value
        })
    
    return list(reversed(historical))

def generate_mock_station_data():
    """Generate mock data for all NYC stations"""
    stations = []
    
    for station in NYC_STATIONS:
        aqi_value = random.randint(40, 120)
        
        stations.append({
            "id": station["id"],
            "location": station["location"],
            "latitude": station["latitude"],
            "longitude": station["longitude"],
            "aqi_value": aqi_value,
            "aqi_category": get_aqi_category(aqi_value),
            "primary_pollutant": "PM2.5",
            "pm25": round(random.uniform(10, 30), 1),
            "pm10": round(random.uniform(15, 40), 1),
            "o3": round(random.uniform(20, 60), 1),
            "no2": round(random.uniform(10, 35), 1),
            "so2": round(random.uniform(5, 15), 1),
            "co": round(random.uniform(0.5, 2.0), 1),
            "temperature": round(random.uniform(15, 25), 1),
            "humidity": round(random.uniform(50, 80), 1),
            "reading_time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        })
    
    return stations

# Routes
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "OK",
        "timestamp": datetime.now().isoformat(),
        "environment": "development",
        "version": "1.0.0"
    })

@app.route('/api/aqi/nyc/current', methods=['GET'])
def get_current_aqi():
    """Get current NYC air quality data"""
    try:
        current_data = generate_mock_current_data()
        historical_data = generate_mock_historical_data()
        
        # Save current data to database (for home location)
        db.save_location_data("home", current_data)
        
        response = {
            "current": current_data,
            "historical": historical_data
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/aqi/nyc/stations', methods=['GET'])
def get_stations_data():
    """Get air quality data for all NYC monitoring stations"""
    try:
        stations_data = generate_mock_station_data()
        
        # Save station data to database
        db.save_station_data(stations_data)
        
        # Also save data for each mapped location
        for station in stations_data:
            station_id = station['id']
            if station_id in STATION_TO_LOCATION:
                location_id = STATION_TO_LOCATION[station_id]
                db.save_location_data(location_id, station)
        
        response = {
            "stations": stations_data
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/aqi/nyc/station/<station_id>', methods=['GET'])
def get_station_data(station_id):
    """Get air quality data for a specific station"""
    try:
        station_data = generate_mock_station_data()
        
        # Find the requested station
        station = next((s for s in station_data if s["id"] == station_id), None)
        
        if not station:
            return jsonify({"error": "Station not found"}), 404
        
        return jsonify(station)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/aqi/health-recommendations', methods=['GET'])
def get_health_recommendations():
    """Get health recommendations based on current AQI"""
    try:
        current_data = generate_mock_current_data()
        
        recommendations = {
            "good": {
                "message": "Air quality is satisfactory and poses little or no risk.",
                "activities": ["All outdoor activities are safe", "Great day for outdoor exercise"],
                "sensitive_groups": "No special precautions needed"
            },
            "moderate": {
                "message": "Air quality is acceptable for most people.",
                "activities": ["Most outdoor activities are safe", "Consider reducing prolonged outdoor exertion"],
                "sensitive_groups": "Sensitive individuals may experience minor breathing discomfort"
            },
            "unhealthy_sensitive": {
                "message": "Sensitive groups may experience health effects.",
                "activities": ["Reduce outdoor activities", "Avoid prolonged outdoor exertion"],
                "sensitive_groups": "Children, elderly, and those with respiratory conditions should limit outdoor activities"
            },
            "unhealthy": {
                "message": "Everyone may begin to experience health effects.",
                "activities": ["Avoid outdoor activities", "Stay indoors when possible"],
                "sensitive_groups": "Sensitive groups should avoid all outdoor activities"
            },
            "very_unhealthy": {
                "message": "Health warnings of emergency conditions.",
                "activities": ["Stay indoors", "Avoid all outdoor activities"],
                "sensitive_groups": "Everyone should avoid outdoor activities"
            },
            "hazardous": {
                "message": "Health alert: everyone may experience serious health effects.",
                "activities": ["Stay indoors", "Use air purifiers", "Avoid all outdoor activities"],
                "sensitive_groups": "Emergency conditions - everyone should stay indoors"
            }
        }
        
        category = current_data["aqi_category"]
        
        response = {
            "aqi_value": current_data["aqi_value"],
            "aqi_category": category,
            "recommendations": recommendations.get(category, recommendations["moderate"])
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/users/profile', methods=['POST'])
def create_user_profile():
    """Create or update user profile"""
    try:
        data = request.get_json()
        
        # Simple validation
        if not data.get('userId'):
            return jsonify({"error": "User ID is required"}), 400
        
        # Save to database
        success = db.save_user_profile(data.get('userId'), data)
        
        if success:
            response = {
                "message": "User profile saved successfully",
                "profile": {
                    "userId": data.get('userId'),
                    "age": data.get('age'),
                    "sex": data.get('sex'),
                    "smoking_status": data.get('smoking_status'),
                    "health_conditions": data.get('health_conditions', []),
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
            }
            return jsonify(response)
        else:
            return jsonify({"error": "Failed to save profile"}), 500
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/users/profile/<user_id>', methods=['GET'])
def get_user_profile(user_id):
    """Get user profile by ID"""
    try:
        # Fetch from database
        profile = db.get_user_profile(user_id)
        
        if profile:
            return jsonify(profile)
        else:
            return jsonify({"error": "User profile not found"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/users/profile/<user_id>/health-risk', methods=['GET'])
def get_health_risk(user_id):
    """Get user's health risk assessment"""
    try:
        # Mock health risk assessment
        risk_level = "moderate"
        aqi_threshold = 75
        
        response = {
            "userId": user_id,
            "risk_level": risk_level,
            "recommended_aqi_threshold": aqi_threshold,
            "profile_summary": {
                "age": 30,
                "smoking_status": "never",
                "health_conditions": ["asthma"]
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/location/<location_id>/current', methods=['GET'])
def get_location_current_data(location_id):
    """Get current air quality data for a specific location"""
    try:
        if location_id not in LOCATION_MAPPING:
            return jsonify({"error": "Invalid location"}), 400
        
        # Get latest data from database
        data = db.get_latest_location_data(location_id)
        
        if data:
            return jsonify(data)
        else:
            return jsonify({"error": "No data available for this location"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/location/<location_id>/history', methods=['GET'])
def get_location_history(location_id):
    """Get historical data for a specific location"""
    try:
        if location_id not in LOCATION_MAPPING:
            return jsonify({"error": "Invalid location"}), 400
        
        hours = request.args.get('hours', 24, type=int)
        data = db.get_location_history(location_id, hours)
        
        return jsonify({
            "location": location_id,
            "hours": hours,
            "data": data
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/database/stats', methods=['GET'])
def get_database_stats():
    """Get database statistics"""
    try:
        stats = db.get_database_stats()
        return jsonify({
            "message": "Database statistics",
            "stats": stats,
            "location_mapping": LOCATION_MAPPING
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_air_quality_insight(location_data):
    """Generate custom air quality insights using Ollama with full location data"""
    try:
        # Ollama API endpoint (assuming it's running locally)
        ollama_url = "http://localhost:11434/api/generate"
        
        # Extract key data for the prompt
        display_location = location_data.get('location', 'Unknown Location')
        aqi_value = location_data.get('aqi_value', 0)
        aqi_category = location_data.get('aqi_category', 'Unknown')
        primary_pollutant = location_data.get('primary_pollutant', 'Unknown')
        
        # Air quality measurements
        pm25 = location_data.get('pm25', 0)
        pm10 = location_data.get('pm10', 0)
        o3 = location_data.get('o3', 0)
        no2 = location_data.get('no2', 0)
        so2 = location_data.get('so2', 0)
        co = location_data.get('co', 0)
        temperature = location_data.get('temperature', 0)
        humidity = location_data.get('humidity', 0)
        
        # Create a comprehensive prompt
        prompt = f"""You are an air quality expert providing personalized insights. Analyze the following air quality data for {display_location} and provide 2-3 actionable insights.

AIR QUALITY DATA:
- Location: {display_location}
- Overall AQI: {aqi_value} ({aqi_category})
- Primary Pollutant: {primary_pollutant}
- PM2.5: {pm25} μg/m³
- PM10: {pm10} μg/m³
- Ozone (O3): {o3} ppb
- Nitrogen Dioxide (NO2): {no2} ppb
- Sulfur Dioxide (SO2): {so2} ppb
- Carbon Monoxide (CO): {co} ppm
- Temperature: {temperature}°C
- Humidity: {humidity}%

INSTRUCTIONS:
- Provide 2-3 short, actionable insights (1-2 sentences each)
- Use normal English - refer to the area as "{display_location}"
- Consider specific pollutants and their health impacts
- Include practical recommendations (e.g., "check for nearby fires" if CO is high)
- Be conversational and helpful
- Focus on what the person should do right now
- Make each insight unique and specific to the current conditions

Generate insights:"""
        
        payload = {
            "model": "llama2",  # or whatever model you have
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.8,  # Add some randomness for fresh insights
                "top_p": 0.9
            }
        }
        
        response = requests.post(ollama_url, json=payload, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('response', generate_fallback_insight(location_data))
        else:
            # Fallback if Ollama is not available
            return generate_fallback_insight(location_data)
            
    except Exception as e:
        print(f"❌ Error generating insight with Ollama: {e}")
        # Fallback if Ollama is not available
        return generate_fallback_insight(location_data)

def generate_fallback_insight(location_data):
    """Generate fallback insights when Ollama is not available"""
    display_location = location_data.get('location', 'Unknown Location')
    aqi_value = location_data.get('aqi_value', 0)
    aqi_category = location_data.get('aqi_category', 'Unknown')
    primary_pollutant = location_data.get('primary_pollutant', 'Unknown')
    co = location_data.get('co', 0)
    pm25 = location_data.get('pm25', 0)
    temperature = location_data.get('temperature', 0)
    
    # Generate insights based on specific pollutants and conditions
    insights = []
    
    # AQI-based general insight
    if aqi_category == "Good":
        insights.append(f"Air quality is excellent in {display_location} - perfect for outdoor activities!")
    elif aqi_category == "Moderate":
        insights.append(f"Air quality is acceptable in {display_location} - most activities are safe")
    elif aqi_category == "Unhealthy for Sensitive Groups":
        insights.append(f"Air quality may affect sensitive groups in {display_location} - limit outdoor time")
    elif aqi_category == "Unhealthy":
        insights.append(f"Air quality is unhealthy in {display_location} - stay indoors when possible")
    elif aqi_category == "Very Unhealthy":
        insights.append(f"Air quality is very unhealthy in {display_location} - stay indoors")
    else:
        insights.append(f"Hazardous air quality in {display_location} - stay indoors immediately")
    
    # Specific pollutant insights
    if co > 2.0:
        insights.append("High CO levels detected - check for nearby fires or gas leaks")
    elif co > 1.0:
        insights.append("Elevated CO levels - avoid areas with heavy traffic")
    
    if pm25 > 25:
        insights.append("High PM2.5 levels - consider wearing a mask outdoors")
    elif pm25 > 15:
        insights.append("Moderate PM2.5 levels - sensitive individuals should take precautions")
    
    if temperature > 30:
        insights.append("Hot weather combined with air pollution - stay hydrated and limit outdoor time")
    elif temperature < 5:
        insights.append("Cold weather may trap pollutants - check indoor air quality")
    
    # Primary pollutant specific advice
    if primary_pollutant == "PM2.5":
        insights.append("Fine particles are the main concern - avoid outdoor exercise")
    elif primary_pollutant == "O3":
        insights.append("Ozone levels are elevated - avoid outdoor activities during peak hours")
    elif primary_pollutant == "NO2":
        insights.append("Nitrogen dioxide from traffic - avoid busy roads")
    
    # Return 2-3 insights
    return "\n".join(insights[:3])

@app.route('/api/insights/<location_id>', methods=['GET'])
def get_location_insights(location_id):
    """Get AI-generated insights for a specific location"""
    try:
        if location_id not in LOCATION_MAPPING:
            return jsonify({"error": "Invalid location"}), 400
        
        # Get current data for the location
        data = db.get_latest_location_data(location_id)
        
        if not data:
            return jsonify({"error": "No data available for this location"}), 404
        
        # Add location name to the data (use display name for user-friendly output)
        location_display_names = {
            'home': 'your home area',
            'work': 'your work area', 
            'football': 'your football center area',
            'studio': 'your studio area',
            'daycare': 'your daycare area'
        }
        data['location'] = location_display_names.get(location_id, LOCATION_MAPPING[location_id])
        
        # Generate insight using full location data
        insight = generate_air_quality_insight(data)
        
        return jsonify({
            "location": LOCATION_MAPPING[location_id],
            "aqi_value": data['aqi_value'],
            "aqi_category": data['aqi_category'],
            "primary_pollutant": data['primary_pollutant'],
            "insight": insight,
            "full_data": data  # Include full data for debugging
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        "message": "AirWatch Backend API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "currentNYC": "/api/aqi/nyc/current",
            "stationsNYC": "/api/aqi/nyc/stations",
            "locationCurrent": "/api/location/:locationId/current",
            "locationHistory": "/api/location/:locationId/history",
            "locationInsights": "/api/insights/:locationId",
            "userProfile": "/api/users/profile",
            "healthRisk": "/api/users/profile/:userId/health-risk",
            "databaseStats": "/api/database/stats"
        },
        "locations": list(LOCATION_MAPPING.keys()),
        "documentation": "Python Flask backend for AirWatch with SQLite database"
    })

if __name__ == '__main__':
    print("🚀 Starting AirWatch Python Backend...")
    print("📊 Environment: development")
    print(f"🌍 NYC Coordinates: {NYC_LAT}, {NYC_LON}")
    print("\n📋 Available endpoints:")
    print("   GET  /health - Health check")
    print("   GET  /api/aqi/nyc/current - Current NYC air quality")
    print("   GET  /api/aqi/nyc/stations - NYC monitoring stations")
    print("   POST /api/users/profile - Create/update user profile")
    print("   GET  /api/users/profile/:userId - Get user profile")
    print("\n🌐 Server URL: http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
