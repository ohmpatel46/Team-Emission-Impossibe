import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional

class AirQualityDatabase:
    def __init__(self, db_path: str = "air_quality.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with tables for each location"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables for each location
        locations = [
            ("home", "Home"),
            ("work", "Work"), 
            ("football", "Football Center"),
            ("studio", "Studio"),
            ("daycare", "Daycare")
        ]
        
        for location_id, location_name in locations:
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {location_id}_air_quality (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    aqi_value INTEGER NOT NULL,
                    aqi_category TEXT NOT NULL,
                    primary_pollutant TEXT NOT NULL,
                    pm25 REAL NOT NULL,
                    pm10 REAL NOT NULL,
                    o3 REAL NOT NULL,
                    no2 REAL NOT NULL,
                    so2 REAL NOT NULL,
                    co REAL NOT NULL,
                    temperature REAL NOT NULL,
                    humidity REAL NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    reading_time TEXT NOT NULL,
                    data_source TEXT DEFAULT 'api'
                )
            """)
        
        # Create a general stations table for NYC monitoring stations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nyc_stations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                station_id TEXT UNIQUE NOT NULL,
                location TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                aqi_value INTEGER NOT NULL,
                aqi_category TEXT NOT NULL,
                primary_pollutant TEXT NOT NULL,
                pm25 REAL NOT NULL,
                pm10 REAL NOT NULL,
                o3 REAL NOT NULL,
                no2 REAL NOT NULL,
                reading_time TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create user profiles table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE NOT NULL,
                age INTEGER,
                sex TEXT,
                smoking_status TEXT,
                health_conditions TEXT, -- JSON array
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully")
    
    def save_location_data(self, location_id: str, data: Dict) -> bool:
        """Save air quality data for a specific location"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(f"""
                INSERT INTO {location_id}_air_quality 
                (aqi_value, aqi_category, primary_pollutant, pm25, pm10, o3, no2, so2, co, 
                 temperature, humidity, latitude, longitude, reading_time, data_source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['aqi_value'],
                data['aqi_category'],
                data['primary_pollutant'],
                data['pm25'],
                data['pm10'],
                data['o3'],
                data['no2'],
                data['so2'],
                data['co'],
                data['temperature'],
                data['humidity'],
                data['latitude'],
                data['longitude'],
                data['reading_time'],
                data.get('data_source', 'api')
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Error saving {location_id} data: {e}")
            return False
    
    def save_station_data(self, station_data: List[Dict]) -> bool:
        """Save NYC monitoring station data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for station in station_data:
                cursor.execute("""
                    INSERT OR REPLACE INTO nyc_stations 
                    (station_id, location, latitude, longitude, aqi_value, aqi_category, 
                     primary_pollutant, pm25, pm10, o3, no2, so2, co, reading_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    station['id'],
                    station['location'],
                    station['latitude'],
                    station['longitude'],
                    station['aqi_value'],
                    station['aqi_category'],
                    station['primary_pollutant'],
                    station['pm25'],
                    station['pm10'],
                    station['o3'],
                    station['no2'],
                    station['reading_time']
                ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Error saving station data: {e}")
            return False
    
    def get_latest_location_data(self, location_id: str) -> Optional[Dict]:
        """Get the latest air quality data for a location"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(f"""
                SELECT * FROM {location_id}_air_quality 
                ORDER BY timestamp DESC LIMIT 1
            """)
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                columns = [description[0] for description in cursor.description]
                return dict(zip(columns, row))
            return None
        except Exception as e:
            print(f"❌ Error getting {location_id} data: {e}")
            return None
    
    def get_location_history(self, location_id: str, hours: int = 24) -> List[Dict]:
        """Get historical data for a location"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # For demo purposes, return all data from September 14-20, 2025
            cursor.execute(f"""
                SELECT * FROM {location_id}_air_quality 
                WHERE reading_time >= '2025-09-14T00:00:00Z' 
                AND reading_time <= '2025-09-20T23:59:59Z'
                ORDER BY reading_time DESC
            """)
            
            rows = cursor.fetchall()
            conn.close()
            
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f"❌ Error getting {location_id} history: {e}")
            return []
    
    def get_all_stations_data(self) -> List[Dict]:
        """Get all NYC station data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM nyc_stations ORDER BY timestamp DESC")
            rows = cursor.fetchall()
            conn.close()
            
            columns = [description[0] for description in cursor.description]
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            print(f"❌ Error getting stations data: {e}")
            return []
    
    def save_user_profile(self, user_id: str, profile_data: Dict) -> bool:
        """Save user profile data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO user_profiles 
                (user_id, age, sex, smoking_status, health_conditions, updated_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                user_id,
                profile_data.get('age'),
                profile_data.get('sex'),
                profile_data.get('smoking_status'),
                json.dumps(profile_data.get('health_conditions', []))
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Error saving user profile: {e}")
            return False
    
    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """Get user profile data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM user_profiles WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                columns = [description[0] for description in cursor.description]
                profile = dict(zip(columns, row))
                # Parse health_conditions JSON
                if profile['health_conditions']:
                    profile['health_conditions'] = json.loads(profile['health_conditions'])
                return profile
            return None
        except Exception as e:
            print(f"❌ Error getting user profile: {e}")
            return None
    
    def get_database_stats(self) -> Dict:
        """Get database statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            stats = {}
            locations = ["home", "work", "football", "studio", "daycare"]
            
            for location in locations:
                cursor.execute(f"SELECT COUNT(*) FROM {location}_air_quality")
                count = cursor.fetchone()[0]
                stats[f"{location}_records"] = count
            
            cursor.execute("SELECT COUNT(*) FROM nyc_stations")
            stats["station_records"] = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM user_profiles")
            stats["user_profiles"] = cursor.fetchone()[0]
            
            conn.close()
            return stats
        except Exception as e:
            print(f"❌ Error getting database stats: {e}")
            return {}

# Location mapping to NYC monitoring stations
LOCATION_MAPPING = {
    "home": "manhattan_midtown",      # Home -> Manhattan Midtown
    "work": "brooklyn_downtown",      # Work -> Brooklyn Downtown  
    "football": "queens_astoria",    # Football Center -> Queens Astoria
    "studio": "bronx_south",         # Studio -> Bronx South
    "daycare": "staten_island_north" # Daycare -> Staten Island North
}

# Reverse mapping for API responses
STATION_TO_LOCATION = {v: k for k, v in LOCATION_MAPPING.items()}
