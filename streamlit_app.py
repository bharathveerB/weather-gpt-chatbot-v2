import streamlit as st
import requests
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Page configuration
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Hide Streamlit elements */
    .stDeployButton {display: none;}
    footer {visibility: hidden;}
    .stApp > header {visibility: hidden;}
    
    /* Global styling */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main app container */
    .stApp {
        background: linear-gradient(to top, #5ee7df 0%, #b490ca 100%);
        min-height: 100vh;
    }
    
    .main .block-container {
        padding: 2rem 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Dashboard title */
    .dashboard-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 3rem;
        letter-spacing: -0.02em;
    }
    
    /* City tiles container */
    .cities-container {
        display: flex;
        gap: 1.5rem;
        margin-bottom: 4rem;
        justify-content: center;
        flex-wrap: wrap;
        padding: 20px;
   }
    
    /* Individual city tile */
    .city-tile {
        background: #4e619c;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        min-width: 220px;
        border: 1px solid rgba(0, 0, 0, 0.04);
    }
    
    .city-tile:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
    }
    
    .city-name {
        font-size: 2.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .current-temp {
        font-size: 2.5rem;
        font-weight: 700;
        color: #3498db;
        margin: 0.5rem 0;
    }
    
    .weather-desc {
        color: #7f8c8d;
        font-size: 1.5rem;
        margin-bottom: 1rem;
        text-transform: capitalize;
    }
    
    .forecast-row {
        display: flex;
        justify-content: space-between;
        gap: 0.5rem;
    }
    
    .forecast-day {
        text-align: center;
        flex: 1;
        padding: 0.5rem;
        background:linear-gradient(-180deg, rgba(255,255,255,0.50) 0%, rgba(0,0,0,0.50) 100%); background-blend-mode: lighten;
        border-radius: 8px;
    }
    
    .forecast-day-name {
        font-size: 1.5rem;
        color: #7f8c8d
        font-weight: 500;
        margin-bottom: 0.25rem;
    }
    
    .forecast-temp {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
    }
    
    /* Search section */
    .search-section {
        max-width: 600px;
        margin: 0 auto 2rem auto;
        text-align: center;
    }
    
    .search-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    
    /* Custom search input styling */
    .stTextInput > div > div > input {
        background: white;
        border: 2px solid #e1e8ed;
        border-radius: 50px;
        padding: 1rem 1.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        width: 100%;
        color: #333333;
    }
    
    .stTextInput > div > div > input:hover {
        border-color: #42e35a;
        box-shadow: 0 4px 20px rgba(66, 227, 90, 0.15);
        transform: scale(1.05,1.3);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #42e35a;
        box-shadow: 0 4px 20px rgba(66, 227, 90, 0.2);
        outline: none;
        transform: scale(1.05,1.3);
    }
    
    /* Search button */
    .stButton > button {
        color: white;
        border: none;
        border-radius: 50px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
    }
    
    .stButton > button:hover {
        transform: scale(1.2,1.2);
        box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4);
    }
    
    /* Example question buttons */
    div[data-testid="column"] .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem;
        font-weight: 500;
        font-size: 0.9rem;
        line-height: 1.2;
        height: auto;
        min-height: 60px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        text-align: center;
        white-space: normal;
        word-wrap: break-word;
    }
    
    div[data-testid="column"] .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Response container */
    .response-container {
        background: #cf5b5b;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 2rem auto;
        max-width: 800px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(0, 0, 0, 0.04);
    }
    
    .response-text {
        line-height: 1.6;
        font-size: 2rem;
        color: #2c3e50;
    }
    
    /* Weather icons */
    .weather-icon {
        font-size: 2.5rem;
        margin: 0.5rem 0;
        display: block;
        text-align: center;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .cities-container {
            flex-direction: column;
            align-items: center;
        }
        
        .city-tile {
            width: 100%;
            max-width: 300px;
        }
        
        .dashboard-title {
            font-size: 2.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Top 5 global cities
TOP_CITIES = [
    {"name": "New Delhi", "country": "India", "lat": 28.6139, "lon": 77.2090},
    {"name": "New York", "country": "USA", "lat": 40.7128, "lon": -74.0060},
    {"name": "Tokyo", "country": "Japan", "lat": 35.6762, "lon": 139.6503},
    {"name": "Paris", "country": "France", "lat": 48.8566, "lon": 2.3522},
    {"name": "Sydney", "country": "Australia", "lat": -33.8688, "lon": 151.2093}
]

# Example questions for scrolling placeholder
EXAMPLE_QUESTIONS = [
    "What's the weather in New Delhi?",
    "Should I carry an umbrella tomorrow in Hyderabad?",
    "Rain probability in Tokyo this weekend?",
    "Temperature in London right now?",
    "Will it snow in Moscow next week?",
    "Humidity levels in Mumbai today?",
    "Sunset time in Los Angeles?",
    "Wind speed in Chicago?",
    "Weather forecast for Dubai?",
    "Is it sunny in Barcelona?"
]

# Enhanced autocomplete suggestions with cities and fuzzy matching
GLOBAL_CITIES = [
    "New York", "London", "Tokyo", "Paris", "Sydney", "New Delhi", "Mumbai", "Hyderabad",
    "Los Angeles", "Chicago", "Toronto", "Berlin", "Moscow", "Dubai", "Singapore",
    "Hong Kong", "Shanghai", "Beijing", "Seoul", "Bangkok", "Jakarta", "Manila",
    "Cairo", "Lagos", "Johannesburg", "São Paulo", "Mexico City", "Buenos Aires",
    "Lima", "Bogotá", "Miami", "Las Vegas", "San Francisco", "Seattle", "Boston",
    "Atlanta", "Houston", "Phoenix", "Denver", "Montreal", "Vancouver", "Rome",
    "Madrid", "Barcelona", "Amsterdam", "Brussels", "Vienna", "Prague", "Warsaw",
    "Stockholm", "Oslo", "Helsinki", "Copenhagen", "Zurich", "Geneva", "Milan",
    "Venice", "Florence", "Athens", "Istanbul", "Tel Aviv", "Riyadh", "Doha",
    "Kuwait City", "Muscat", "Abu Dhabi", "Karachi", "Lahore", "Islamabad",
    "Dhaka", "Colombo", "Kathmandu", "Kabul", "Tashkent", "Almaty", "Baku",
    "Tbilisi", "Yerevan", "Ankara", "Izmir", "Antalya", "Casablanca", "Tunis",
    "Algiers", "Tripoli", "Khartoum", "Addis Ababa", "Nairobi", "Kampala",
    "Dar es Salaam", "Lusaka", "Harare", "Gaborone", "Windhoek", "Cape Town",
    "Durban", "Port Elizabeth", "Bloemfontein", "Pretoria", "Perth", "Adelaide",
    "Melbourne", "Brisbane", "Darwin", "Canberra", "Auckland", "Wellington",
    "Christchurch", "Suva", "Port Moresby", "Honolulu", "Anchorage", "Fairbanks"
]

WEATHER_KEYWORDS = {
    "temp": ["temperature", "temp", "hot", "cold", "warm", "cool", "degrees", "celsius", "fahrenheit"],
    "rain": ["rain", "rainfall", "precipitation", "drizzle", "shower", "downpour", "wet"],
    "wind": ["wind", "windy", "breeze", "gust", "gale", "storm", "hurricane", "cyclone"],
    "humid": ["humidity", "humid", "moisture", "muggy", "sticky", "damp"],
    "sun": ["sun", "sunny", "sunshine", "bright", "clear", "sunrise", "sunset"],
    "cloud": ["cloud", "cloudy", "overcast", "grey", "gray", "partly cloudy"],
    "snow": ["snow", "snowy", "snowfall", "blizzard", "sleet", "ice", "icy", "frost"],
    "storm": ["storm", "thunderstorm", "lightning", "thunder", "severe weather"],
    "forecast": ["forecast", "prediction", "outlook", "tomorrow", "week", "weekend"],
    "pressure": ["pressure", "barometric", "atmospheric"],
    "visibility": ["visibility", "fog", "mist", "haze", "clear"]
}

QUERY_TEMPLATES = [
    "What's the weather in {city}?",
    "Temperature in {city}",
    "Rain forecast for {city}",
    "Will it rain in {city}?",
    "Weather forecast for {city}",
    "Humidity in {city}",
    "Wind speed in {city}",
    "Sunrise time in {city}",
    "Sunset in {city}",
    "Snow forecast for {city}",
    "Storm warning for {city}",
    "Weather this week in {city}",
    "Temperature tomorrow in {city}",
    "Should I carry an umbrella in {city}?",
    "Is it sunny in {city}?",
    "Probability of rain in {city}",
    "Weather conditions in {city}"
]

class WeatherAPI:
    def __init__(self):
        self.base_url = "http://localhost:8000"
    
    def get_weather_data(self, lat: float, lon: float) -> Dict[str, Any]:
        """Get weather data from Open-Meteo API"""
        try:
            url = f"https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": ["temperature_2m", "relative_humidity_2m", "weather_code", "wind_speed_10m"],
                "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "precipitation_probability_max"],
                "forecast_days": 7,
                "timezone": "auto"
            }
            response = requests.get(url, params=params)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            st.error(f"Error fetching weather data: {e}")
            return None
    
    def ask_weather_question(self, question: str) -> str:
        """Ask weather question to FastAPI backend"""
        try:
            response = requests.post(
                f"{self.base_url}/ask",
                json={"question": question},
                timeout=30
            )
            if response.status_code == 200:
                return response.json().get("answer", "No response received")
            else:
                return f"Error: {response.status_code} - {response.text}"
        except requests.exceptions.ConnectionError:
            return "⚠️ Backend server not running. Please start the FastAPI server first."
        except Exception as e:
            return f"Error: {str(e)}"

def get_weather_icon(weather_code: int) -> str:
    """Get weather icon based on weather code"""
    icons = {
        0: "☀️",  # Clear sky
        1: "🌤️",  # Mainly clear
        2: "⛅",  # Partly cloudy
        3: "☁️",  # Overcast
        45: "🌫️", # Fog
        48: "🌫️", # Depositing rime fog
        51: "🌦️", # Light drizzle
        53: "🌦️", # Moderate drizzle
        55: "🌧️", # Dense drizzle
        61: "🌧️", # Slight rain
        63: "🌧️", # Moderate rain
        65: "🌧️", # Heavy rain
        71: "🌨️", # Slight snow
        73: "🌨️", # Moderate snow
        75: "❄️",  # Heavy snow
        95: "⛈️",  # Thunderstorm
        96: "⛈️",  # Thunderstorm with hail
        99: "⛈️"   # Thunderstorm with heavy hail
    }
    return icons.get(weather_code, "🌤️")

def get_weather_animation_class(weather_code: int) -> str:
    """Get CSS animation class based on weather code"""
    if weather_code == 0:
        return "sun-animation"
    elif weather_code in [51, 53, 55, 61, 63, 65]:
        return "rain-animation"
    elif weather_code in [2, 3, 45, 48]:
        return "cloud-animation"
    else:
        return "float"

def display_city_weather(city: Dict[str, Any], weather_data: Dict[str, Any]):
    """Display compact weather card for a city"""
    if not weather_data:
        st.markdown(f"""
        <div class="weather-card">
            <div style="text-align: center;">
                <h4>{city['name']}</h4>
                <p style="color: rgba(255,255,255,0.7);">Data unavailable</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    current = weather_data.get("current", {})
    daily = weather_data.get("daily", {})
    
    temp = current.get("temperature_2m", 0)
    humidity = current.get("relative_humidity_2m", 0)
    wind_speed = current.get("wind_speed_10m", 0)
    weather_code = current.get("weather_code", 0)
    
    icon = get_weather_icon(weather_code)
    animation_class = get_weather_animation_class(weather_code)
    
    st.markdown(f"""
    <div class="weather-card">
        <div style="text-align: center;">
            <h5 style="margin: 0 0 5px 0; font-size: 1.5rem;">{city['name']}</h5>
            <div class="weather-icon {animation_class}" style="font-size: 2rem; margin: 3px 0;">{icon}</div>
            <h4 style="margin: 3px 0; font-size: 1.3rem;">{temp:.1f}°C</h4>
            <p style="margin: 3px 0; font-size: 1rem; color: rgba(255,255,255,0.8);">💧{humidity}% 💨{wind_speed:.0f}km/h</p>
        </div>
        <div class="forecast-carousel">
    """, unsafe_allow_html=True)
    
    # Ultra compact 3-day forecast to save space
    if daily and "time" in daily:
        for i in range(min(3, len(daily["time"]))):
            date = datetime.fromisoformat(daily["time"][i]).strftime("%a")
            max_temp = daily["temperature_2m_max"][i] if i < len(daily["temperature_2m_max"]) else 0
            min_temp = daily["temperature_2m_min"][i] if i < len(daily["temperature_2m_min"]) else 0
            day_weather_code = daily["weather_code"][i] if i < len(daily["weather_code"]) else 0
            day_icon = get_weather_icon(day_weather_code)
            
            st.markdown(f"""
            <div class="forecast-day">
                <div style="font-size: 1rem;text-align: left;">{date}</div>
                <div style="font-size: 1rem; margin: 1px 0;">{day_icon}</div>
                <div style="font-size: 1rem;text-align: right;">{max_temp:.0f}°/{min_temp:.0f}°</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def get_autocomplete_suggestions(query: str) -> List[str]:
    """Get smart autocomplete suggestions with fuzzy matching"""
    if not query or len(query) < 2:
        return []
    
    suggestions = set()
    query_lower = query.lower().strip()
    
    # 1. Direct city matches
    matching_cities = []
    for city in GLOBAL_CITIES:
        city_lower = city.lower()
        if query_lower in city_lower or city_lower.startswith(query_lower):
            matching_cities.append(city)
    
    # Add city-based suggestions
    for city in matching_cities[:8]:  # Limit cities
        for template in QUERY_TEMPLATES[:6]:  # Limit templates per city
            suggestions.add(template.format(city=city))
    
    # 2. Weather keyword matches
    for category, keywords in WEATHER_KEYWORDS.items():
        for keyword in keywords:
            if query_lower in keyword or keyword.startswith(query_lower):
                # Add generic suggestions for this weather type
                if category == "temp":
                    suggestions.update([
                        f"Temperature in London",
                        f"Temperature forecast",
                        f"Temperature conversion",
                        f"Hot weather today",
                        f"Cold weather alert"
                    ])
                elif category == "rain":
                    suggestions.update([
                        f"Rain forecast for Paris",
                        f"Probability of rain in New Delhi",
                        f"Will it rain tomorrow?",
                        f"Rainfall this week",
                        f"Rain in Tokyo"
                    ])
                elif category == "wind":
                    suggestions.update([
                        f"Wind speed in Chicago",
                        f"Windy weather forecast",
                        f"Wind direction today",
                        f"Storm warning"
                    ])
                elif category == "forecast":
                    suggestions.update([
                        f"Weather forecast for New York",
                        f"7-day forecast",
                        f"Tomorrow's weather",
                        f"Weekend weather outlook"
                    ])
                break
    
    # 3. Fuzzy matching for partial words
    if len(query_lower) >= 3:
        for city in GLOBAL_CITIES:
            # Check if any word in city name contains the query
            city_words = city.lower().split()
            for word in city_words:
                if query_lower in word:
                    suggestions.add(f"Weather in {city}")
                    suggestions.add(f"Temperature in {city}")
                    break
    
    # 4. Smart contextual suggestions
    contextual_suggestions = {
        "hot": ["Hot weather cities", "Heat index today", "Hottest temperature"],
        "cold": ["Cold weather alert", "Coldest cities", "Freezing temperature"],
        "umbrella": ["Should I carry an umbrella?", "Rain probability today"],
        "jacket": ["Do I need a jacket?", "Temperature tonight"],
        "weekend": ["Weekend weather forecast", "Saturday weather", "Sunday forecast"],
        "tomorrow": ["Tomorrow's weather", "Temperature tomorrow", "Rain tomorrow"],
        "today": ["Today's weather", "Current temperature", "Weather right now"],
        "week": ["This week's forecast", "7-day weather outlook", "Weekly weather"]
    }
    
    for key, values in contextual_suggestions.items():
        if query_lower in key or key.startswith(query_lower):
            suggestions.update(values)
    
    # Convert to list and sort by relevance (shorter suggestions first, then alphabetical)
    suggestion_list = list(suggestions)
    suggestion_list.sort(key=lambda x: (len(x), x.lower()))
    
    return suggestion_list[:8]  # Return top 8 suggestions

def main():
    # Initialize weather API
    weather_api = WeatherAPI()
    
    # Initialize session state
    if 'weather_response' not in st.session_state:
        st.session_state.weather_response = ""
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ""
    if 'suggestions' not in st.session_state:
        st.session_state.suggestions = []
    if 'query_made' not in st.session_state:
        st.session_state.query_made = False
    
    # Main container with proper layout
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Compact main title
    st.markdown("<h1 class='main-title' style='text-align: center; color: white; margin-bottom: 10px;'>🌤️ Weather Hub</h1>", unsafe_allow_html=True)
    
    # Cities section - MOVED TO TOP
    st.markdown('<div class="cities-section">', unsafe_allow_html=True)
    st.markdown("<h2 class='section-title' style='text-align: center; color: white; margin: 5px 0;'>Global Weather</h2>", unsafe_allow_html=True)
    
    # Create a compact grid layout for cities
    st.markdown('<div class="cities-grid">', unsafe_allow_html=True)
    cols = st.columns(5)
    
    for i, city in enumerate(TOP_CITIES):
        with cols[i]:
            weather_data = weather_api.get_weather_data(city["lat"], city["lon"])
            display_city_weather(city, weather_data)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close cities-grid
    st.markdown('</div>', unsafe_allow_html=True)  # Close cities-section
    
    # Query section - Show example questions initially, then search bar after first query
    if not st.session_state.query_made:
        # Show example question buttons
        st.markdown('<div class="search-section">', unsafe_allow_html=True)
        st.markdown('<h2 style="text-align: center; color: white; margin: 20px 0;">Try these popular weather queries:</h2>', unsafe_allow_html=True)
        
        # Display 6 example questions as buttons in 2 rows of 3
        example_questions = EXAMPLE_QUESTIONS[:6]  # Take first 6 questions
        
        # First row - 3 buttons
        col1, col2, col3 = st.columns(3)
        for i, question in enumerate(example_questions[:3]):
            with [col1, col2, col3][i]:
                if st.button(question, key=f"example_{i}", use_container_width=True):
                    with st.spinner("Getting weather..."):
                        response = weather_api.ask_weather_question(question)
                        st.session_state.weather_response = response
                        st.session_state.search_query = question
                        st.session_state.query_made = True
                        st.rerun()
        
        # Second row - 3 buttons
        col4, col5, col6 = st.columns(3)
        for i, question in enumerate(example_questions[3:6]):
            with [col4, col5, col6][i]:
                if st.button(question, key=f"example_{i+3}", use_container_width=True):
                    with st.spinner("Getting weather..."):
                        response = weather_api.ask_weather_question(question)
                        st.session_state.weather_response = response
                        st.session_state.search_query = question
                        st.session_state.query_made = True
                        st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close search-section
    
    # Response section (show after query is made)
    if st.session_state.weather_response and st.session_state.query_made:
        st.markdown('<div class="response-section">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="response-container">
            <div style="color: white; font-size: 20px; line-height: 1.3;">{st.session_state.weather_response}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Search section - Show after first query is made
    if st.session_state.query_made:
        st.markdown('<div class="search-section">', unsafe_allow_html=True)
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align: center; color: white; margin: 20px 0;">Ask more weather questions:</h3>', unsafe_allow_html=True)
        
        # Search input with real-time suggestions
        search_col1, search_col2 = st.columns([4, 1])
        
        with search_col1:
            search_query = st.text_input(
                "",
                placeholder="Ask about weather... (e.g., 'Temperature in London')",
                key="search_input",
                label_visibility="collapsed"
            )
        
        with search_col2:
            search_button = st.button("🔍 Ask", use_container_width=True, type="primary")
        
        # Compact autocomplete suggestions
        if search_query and len(search_query) >= 2:
            suggestions = get_autocomplete_suggestions(search_query)
            if suggestions:
                suggestion_cols = st.columns(min(4, len(suggestions)))
                for i, suggestion in enumerate(suggestions[:4]):
                    with suggestion_cols[i]:
                        if st.button(suggestion[:25] + ".." if len(suggestion) > 25 else suggestion, 
                                   key=f"sugg_{i}", use_container_width=True):
                            with st.spinner("Getting weather..."):
                                response = weather_api.ask_weather_question(suggestion)
                                st.session_state.weather_response = response
                                st.session_state.search_query = suggestion
                                st.rerun()
        
        # Process search query
        if search_button and search_query.strip():
            with st.spinner("Getting weather information..."):
                response = weather_api.ask_weather_question(search_query.strip())
                st.session_state.weather_response = response
                st.session_state.search_query = search_query
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close search-container
        st.markdown('</div>', unsafe_allow_html=True)  # Close search-section
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-content

if __name__ == "__main__":
    main()
