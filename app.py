from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import re
import os
import json
from datetime import datetime
from weather_agent import WeatherAgent
from openai import OpenAI
from dotenv import load_dotenv
import uvicorn
import os
# Load environment variables
load_dotenv()

# FastAPI app instance
app = FastAPI(title="Weather Chatbot API", description="AI-powered weather chatbot API", version="1.0.0")

# Request/Response models
class QuestionRequest(BaseModel):
    question: str

class WeatherResponse(BaseModel):
    answer: str
    success: bool = True

class WeatherChatbot:
    def __init__(self):
        self.weather_agent = WeatherAgent()
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found! Please add your API key to the .env file.")
        self.client = OpenAI(api_key=api_key)
    
    def is_weather_question(self, question):
        """Use GPT-4 to intelligently detect if the question is weather-related"""
        try:
            system_prompt = """
            You are a weather intent classifier. Your job is to determine if a user's question is related to weather or not.
            
            Weather-related questions include:
            - Current weather conditions
            - Weather forecasts
            - Temperature inquiries
            - Precipitation (rain, snow, etc.)
            - Weather phenomena (storms, fog, etc.)
            - Climate information
            - Seasonal weather
            
            Respond with ONLY a JSON object: {"is_weather": true} or {"is_weather": false}
            No explanations, just the JSON.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Question: {question}"}
                ],
                temperature=0,
                max_tokens=50
            )
            
            result = json.loads(response.choices[0].message.content.strip())
            return result.get("is_weather", False)
            
        except Exception as e:
            print(f"Error with GPT-4 intent detection: {e}")
            # Fallback to simple keyword detection
            weather_keywords = ['weather', 'temperature', 'rain', 'snow', 'forecast', 'sunny', 'cloudy']
            return any(keyword in question.lower() for keyword in weather_keywords)
    
    def extract_location_from_question(self, question):
        """Use GPT-4 to intelligently extract location from the question"""
        try:
            system_prompt = """
            You are a location extractor. Extract the location/city name from weather-related questions.
            
            Examples:
            - "What's the weather in Paris?" → {"location": "Paris"}
            - "How's the temperature in New York City?" → {"location": "New York City"}
            - "Weather forecast for Tokyo, Japan" → {"location": "Tokyo, Japan"}
            - "Is it raining in London?" → {"location": "London"}
            - "What's the weather like?" → {"location": null}
            
            Respond with ONLY a JSON object: {"location": "city_name"} or {"location": null}
            No explanations, just the JSON.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Question: {question}"}
                ],
                temperature=0,
                max_tokens=100
            )
            
            result = json.loads(response.choices[0].message.content.strip())
            return result.get("location")
            
        except Exception as e:
            print(f"Error with GPT-4 location extraction: {e}")
            # Fallback to simple regex
            location_match = re.search(r'\bin\s+([a-zA-Z\s,]+)', question, re.IGNORECASE)
            if location_match:
                return location_match.group(1).strip()
            return None
    
    def get_coordinates(self, location):
        """Get latitude and longitude for a location using geocoding API"""
        try:
            # Using OpenStreetMap Nominatim API for geocoding (free)
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': location,
                'format': 'json',
                'limit': 1
            }
            headers = {'User-Agent': 'WeatherChatbot/1.0'}
            
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            
            if data:
                return float(data[0]['lat']), float(data[0]['lon'])
            return None, None
        except Exception as e:
            st.error(f"Error getting coordinates: {e}")
            return None, None
    
    def format_weather_response(self, weather_data, location, original_question):
        """Use GPT-4 to generate intelligent, contextual weather responses"""
        if not weather_data:
            return f"Sorry, I couldn't get weather information for {location}. Please check the location name."
        
        try:
            # Prepare weather data for GPT-4
            weather_info = ""
            if 'current_weather' in weather_data:
                current = weather_data['current_weather']
                temp = current['temperature']
                description = current['weather_description']
                weather_info = f"Current weather in {location}: {temp['value']}{temp['unit']}, {description}"
            
            elif 'daily_forecast' in weather_data:
                forecast = weather_data['daily_forecast']
                weather_info = f"Weather forecast for {location}:\n"
                for day in forecast[:3]:  # Show first 3 days
                    date = datetime.strptime(day['date'], '%Y-%m-%d').strftime('%A')
                    min_temp = day['temperature']['min']
                    max_temp = day['temperature']['max']
                    description = day['weather_description']
                    weather_info += f"{date}: {min_temp['value']}-{max_temp['value']}{max_temp['unit']}, {description}\n"
            
            # Use GPT-4 to generate contextual response
            system_prompt = f"""
            You are a helpful weather assistant. Answer the user's weather question using the provided weather data.
            
            Guidelines:
            - Give practical, actionable advice based on the weather
            - If they ask about umbrellas, consider rain/precipitation
            - If they ask about clothing, consider temperature and conditions
            - If they ask about activities, consider the weather impact
            - Be conversational and helpful
            - Include relevant emojis
            - Keep responses concise but informative
            
            Weather Data: {weather_info}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": original_question}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            st.error(f"Error generating intelligent response: {e}")
            # Fallback to basic formatting
            if 'current_weather' in weather_data:
                current = weather_data['current_weather']
                temp = current['temperature']
                description = current['weather_description']
                return f"🌤️ **Current weather in {location}:**\n\n" \
                       f"**Temperature:** {temp['value']}{temp['unit']}\n" \
                       f"**Condition:** {description.title()}"
            return "Weather information retrieved, but couldn't format the response."
    
    def get_weather_response(self, question):
        """Get weather response for a question"""
        location = self.extract_location_from_question(question)
        
        if not location:
            return "Please specify a location for the weather information. For example: 'What's the weather in New York?'"
        
        # Get coordinates
        lat, lon = self.get_coordinates(location)
        if lat is None or lon is None:
            return f"Sorry, I couldn't find the location '{location}'. Please check the spelling or try a different location."
        
        # Determine if it's a forecast request
        forecast_days = 1
        if any(word in question.lower() for word in ['forecast', 'week', 'days', 'tomorrow']):
            forecast_days = 7
        
        # Get weather data
        weather_data = self.weather_agent.extract_weather_summary(lat, lon, forecast_days)
        
        return self.format_weather_response(weather_data, location, question)
    
    def chat(self, question):
        """Main chat function"""
        if not self.is_weather_question(question):
            return "I can answer only weather questions. Please ask me about weather conditions, temperature, or forecasts for any location!"
        
        return self.get_weather_response(question)

# Initialize the chatbot instance
chatbot = WeatherChatbot()

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Weather Chatbot API",
        "description": "AI-powered weather chatbot using GPT-4 and Open-Meteo API",
        "endpoints": {
            "/ask": "POST - Ask weather questions",
            "/docs": "GET - API documentation"
        },
        "examples": [
            "What's the weather in Paris?",
            "Show me the forecast for New York this week",
            "Is it raining in London?"
        ]
    }

@app.post("/ask", response_model=WeatherResponse)
async def ask_weather(request: QuestionRequest):
    """Ask a weather-related question"""
    try:
        if not request.question or not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        # Get response from chatbot
        answer = chatbot.chat(request.question.strip())
        
        return WeatherResponse(answer=answer, success=True)
    
    except ValueError as e:
        # Handle configuration errors (like missing API key)
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # Handle other errors
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
