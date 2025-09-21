# Team Emission Impossible - NYC Climate & Health Hackathon 2k25

A comprehensive air quality monitoring application that tracks air quality data across multiple NYC locations, provides personalized health recommendations, and offers detailed analytics with AI-powered insights.

## 🌟 Features

- **Real-time Air Quality Monitoring**: Current AQI readings for 5 NYC locations
- **Interactive Dashboard**: Live updates, health recommendations, and location switching
- **Advanced Analytics**: 24-hour and 7-day breakdowns with peak hours detection
- **AI-Powered Insights**: Ollama integration for personalized health recommendations
- **Interactive Map**: ArcGIS maps with station markers and location centering
- **Modern UI**: Dark/light mode, responsive design, and data visualization

## 🏗️ Architecture

- **Frontend**: HTML5/CSS3/JavaScript with Chart.js and ArcGIS Maps
- **Backend**: Flask (Python) with SQLite database
- **AI**: Ollama integration with Llama2 model
- **Database**: SQLite with location-specific tables

## 🚀 Quick Setup

### Prerequisites
- Python 3.8+
- Modern web browser
- Ollama (optional, for AI insights)

### Installation

1. **Clone and setup backend:**
```bash
git clone <repository-url>
cd Team-Emission-Impossibe/backend
pip install -r requirements.txt
python -c "from database import AirQualityDatabase; db = AirQualityDatabase(); db.initialize_db()"
python app.py
```

2. **Setup frontend:**
```bash
cd ../frontend
python -m http.server 8000
# Visit: http://localhost:8000/air-quality-monitor-v3.html
```

3. **Optional - AI setup:**
```bash
ollama pull llama2
ollama serve
```

## 📡 API Endpoints

- `GET /api/aqi/nyc/current` - Current NYC air quality
- `GET /api/aqi/nyc/stations` - All monitoring stations  
- `GET /api/location/{id}/current` - Current data for specific location
- `GET /api/location/{id}/history?hours=24` - Historical data
- `GET /api/insights/{id}` - AI-generated health insights

**Location IDs:** `home`, `work`, `football`, `studio`, `daycare`

## 🛠️ Development Tools

```bash
# View database contents
python view_database.py

# Populate sample data
python populate_all_locations.py

# Test API
curl http://localhost:5000/api/aqi/nyc/current
```

## 📱 Usage

1. **Initial Setup**: Complete health questionnaire and select locations
2. **Dashboard**: View current AQI, health recommendations, and real-time updates
3. **Analytics**: Access 24-hour and 7-day detailed breakdowns
4. **Map**: Interactive NYC air quality map with station data
5. **Location Switching**: Compare different areas or view overall data

## 🔧 Configuration

- **Backend**: Port 5000, Database: `air_quality.db`
- **Frontend**: Backend URL: `http://localhost:5000`
- **AI Model**: llama2 (configurable)
- **Update Interval**: 30 seconds

## 📊 Data Sources

- **Mock Data**: Realistic AQI values (0-300) with multiple pollutants
- **Location Mapping**: User-friendly names (Home, Work, Football Center, Studio, Daycare)
- **Historical Data**: Time-series data with proper timestamps
- **Environmental Factors**: Temperature, humidity, and pollutant levels

## 🤖 AI Integration

- **Ollama**: Local LLM deployment with Llama2
- **Context-Aware**: Recommendations based on specific pollutants and conditions
- **Location-Specific**: Tailored advice for each area
- **Fresh Insights**: New recommendations generated for each location selection

## 🎯 Key Features

### ✅ Completed
- Real-time air quality monitoring
- Multi-location data tracking
- Interactive dashboard and analytics
- AI-powered health recommendations
- Interactive map with station data
- Dark/light mode toggle
- Database persistence
- RESTful API design
- Responsive UI design
- Data visualization charts
- Historical data analysis
- Location comparison tools

### 🔮 Future Enhancements
- Real API integration (WeatherAPI, AirNow)
- User authentication
- Mobile app development
- Advanced ML predictions
- Notification system

## 🐛 Troubleshooting

- **Backend not starting**: Check Python version and dependencies
- **Database errors**: Run database initialization script
- **AI insights not working**: Ensure Ollama is running
- **Frontend not loading**: Check backend server status
- **Map not displaying**: Verify internet connection

## 📄 License

MIT License - see LICENSE file for details.

---

*Built with ❤️ for better air quality awareness and public health*