# AirWatch Python Backend

A Python Flask backend for the AirWatch air quality monitoring application with SQLite database integration.

## Features

- 🌍 Mock air quality data for NYC
- 📊 Historical air quality trends (24 hours)
- 🏢 Multiple monitoring station support
- 👤 User profile management
- 🗄️ SQLite database for data persistence
- 📍 Location-based data tracking (5 user locations)
- 🔄 CORS enabled for frontend integration
- 🐍 Simple Python setup

## Quick Start

### 1. Install Python Dependencies

```bash
cd backend_python
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 3. Test the API

```bash
python test_api.py
```

### 4. Populate Database (Optional)

```bash
python populate_database.py
```

### 5. View Database Contents

```bash
python view_database.py
```

Or open your browser and go to:
- `http://localhost:5000/health` - Health check
- `http://localhost:5000/api/aqi/nyc/current` - Current NYC air quality
- `http://localhost:5000/api/aqi/nyc/stations` - NYC monitoring stations
- `http://localhost:5000/api/database/stats` - Database statistics

## API Endpoints

### Required Endpoints (as specified)

#### 1. Get Current & Historical NYC Air Quality
- **Path:** `/api/aqi/nyc/current`
- **Method:** `GET`
- **Response:** Current AQI data + 24 hours of historical data

#### 2. Get Data for All NYC Monitoring Stations
- **Path:** `/api/aqi/nyc/stations`
- **Method:** `GET`
- **Response:** Array of all NYC monitoring stations with current AQI

### Additional Endpoints

- `GET /health` - Health check
- `GET /api/aqi/nyc/station/:stationId` - Specific station data
- `GET /api/aqi/health-recommendations` - Health recommendations
- `POST /api/users/profile` - Create/update user profile
- `GET /api/users/profile/:userId` - Get user profile
- `GET /api/users/profile/:userId/health-risk` - Health risk assessment

### Database Endpoints

- `GET /api/location/:locationId/current` - Current data for specific location
- `GET /api/location/:locationId/history?hours=24` - Historical data for location
- `GET /api/database/stats` - Database statistics and location mapping

## Data Models

### UserProfile
```json
{
  "userId": "string",
  "age": "number",
  "sex": "male|female|other",
  "smoking_status": "never|former|current",
  "health_conditions": ["asthma", "copd", ...]
}
```

### AQIReading
```json
{
  "location": "string",
  "aqi_value": "number",
  "aqi_category": "good|moderate|unhealthy_sensitive|unhealthy|very_unhealthy|hazardous",
  "primary_pollutant": "string",
  "pm25": "number",
  "pm10": "number",
  "o3": "number",
  "no2": "number",
  "so2": "number",
  "co": "number",
  "temperature": "number",
  "humidity": "number",
  "reading_time": "ISO8601 timestamp",
  "latitude": "number",
  "longitude": "number"
}
```

## Frontend Integration

Update your frontend to use port 5000:

```javascript
const BACKEND_CONFIG = {
    baseUrl: 'http://localhost:5000',
    endpoints: {
        airQuality: '/api/aqi/nyc/current',
        stations: '/api/aqi/nyc/stations',
        userProfile: '/api/users/profile',
        deviceStatus: '/health'
    }
};
```

## Example Responses

### Current AQI Response
```json
{
  "current": {
    "location": "New York City, NY",
    "aqi_value": 78,
    "aqi_category": "moderate",
    "primary_pollutant": "PM2.5",
    "pm25": 18.5,
    "pm10": 25.3,
    "o3": 45.2,
    "no2": 22.1,
    "so2": 8.7,
    "co": 1.2,
    "temperature": 22.5,
    "humidity": 65.3,
    "reading_time": "2024-01-15T10:30:00Z",
    "latitude": 40.7128,
    "longitude": -74.0060
  },
  "historical": [
    { "time": "11:00", "aqi": 75 },
    { "time": "12:00", "aqi": 78 }
  ]
}
```

### Stations Response
```json
{
  "stations": [
    {
      "id": "manhattan_midtown",
      "location": "Manhattan Midtown",
      "latitude": 40.7589,
      "longitude": -73.9851,
      "aqi_value": 78,
      "aqi_category": "moderate",
      "primary_pollutant": "PM2.5",
      "pm25": 18.5,
      "pm10": 25.3,
      "o3": 45.2,
      "no2": 22.1,
      "reading_time": "2024-01-15T10:30:00Z"
    }
  ]
}
```

## Database Structure

The SQLite database (`air_quality.db`) contains the following tables:

### Location Tables (5 tables)
- `home_air_quality` - Home location data
- `work_air_quality` - Work location data  
- `football_air_quality` - Football Center data
- `studio_air_quality` - Studio data
- `daycare_air_quality` - Daycare data

Each location table stores:
- AQI values, categories, pollutants
- PM2.5, PM10, O3, NO2, SO2, CO levels
- Temperature, humidity
- Timestamps and coordinates

### Other Tables
- `nyc_stations` - NYC monitoring station data
- `user_profiles` - User health profiles

### Location Mapping
- **Home** → Manhattan Midtown
- **Work** → Brooklyn Downtown
- **Football Center** → Queens Astoria
- **Studio** → Bronx South
- **Daycare** → Staten Island North

## Database Tools

- `view_database.py` - View all database contents
- `populate_database.py` - Populate with initial demo data
- `database.py` - Database class with all operations

## Development

The server runs in debug mode by default, so it will automatically reload when you make changes to the code.

## License

MIT License
