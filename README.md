# Weather GPT Chatbot 🌤️

An intelligent weather dashboard and chatbot that combines the power of GPT-4 with real-time weather data. Features a beautiful Streamlit frontend with global weather tiles and a FastAPI backend for intelligent weather conversations.

![Weather Dashboard](https://img.shields.io/badge/Status-Active-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red) ![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)

## ✨ Features

### 🎨 Beautiful Dashboard
- **Global Weather Tiles**: Live weather for top 5 cities (New Delhi, New York, London, Tokyo, Sydney)
- **Modern UI**: Gradient backgrounds, smooth animations, and responsive design
- **Interactive Elements**: Hover effects and smooth transitions

### 🤖 Intelligent Chatbot
- **GPT-4 Powered**: Uses OpenAI's GPT-4 for natural language understanding
- **Smart Intent Detection**: Accurately identifies weather-related questions
- **Location Extraction**: Intelligently extracts locations from conversational queries
- **Contextual Responses**: Generates human-like, contextual weather responses

### 🌍 Weather Data
- **Real-time Data**: Current weather conditions and forecasts
- **Global Coverage**: Weather for any city worldwide
- **7-day Forecasts**: Extended weather predictions
- **Multiple Parameters**: Temperature, humidity, wind, precipitation, and more

## 🏗️ Architecture

This project uses a modern microservices architecture:

```
┌─────────────────┐    HTTP Requests    ┌─────────────────┐
│   Streamlit     │ ──────────────────► │   FastAPI       │
│   Frontend      │                     │   Backend       │
│   (Port 8501)   │ ◄────────────────── │   (Port 8000)   │
└─────────────────┘    JSON Responses   └─────────────────┘
         │                                        │
         │                                        │
         ▼                                        ▼
┌─────────────────┐                    ┌─────────────────┐
│   Weather UI    │                    │   GPT-4 +       │
│   Dashboard     │                    │   Weather APIs  │
└─────────────────┘                    └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key (for GPT-4 functionality)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd weatheragent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Start the FastAPI backend**
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:8000`

5. **Start the Streamlit frontend** (in a new terminal)
   ```bash
   streamlit run streamlit_app.py
   ```
   The dashboard will open at `http://localhost:8501`

## 💬 Example Conversations

### Natural Language Queries
```
User: "What's the weather like in Paris today?"
Bot: "🌤️ Current weather in Paris: It's 22°C with partly cloudy skies. Perfect weather for a stroll along the Seine!"

User: "Will I need an umbrella in London tomorrow?"
Bot: "🌧️ Yes, you'll want to bring an umbrella! London is expecting light rain tomorrow with temperatures around 18°C."

User: "Show me the forecast for New York this week"
Bot: "📅 Here's the 7-day forecast for New York: [detailed forecast with daily conditions]"
```

### Smart Intent Detection
```
User: "Tell me a joke"
Bot: "I can answer only weather questions. Please ask me about weather conditions, temperature, or forecasts for any location!"
```

## 📁 Project Structure

```
weatheragent/
├── streamlit_app.py      # Main Streamlit dashboard
├── app.py                # FastAPI backend server
├── weather_agent.py      # Weather data processing
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

### Key Components

- **`streamlit_app.py`**: Beautiful frontend with global weather tiles and chat interface
- **`app.py`**: FastAPI backend with GPT-4 integration and weather endpoints
- **`weather_agent.py`**: Weather data extraction from Open-Meteo API

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key for GPT-4 | Yes |

### API Endpoints

- **GET** `/` - API information and examples
- **POST** `/ask` - Ask weather questions
- **GET** `/docs` - Interactive API documentation

## 🌐 APIs Used

- **[OpenAI GPT-4](https://openai.com/gpt-4)**: Natural language processing and response generation
- **[Open-Meteo API](https://open-meteo.com/)**: Free weather data (no API key required)
- **[Nominatim API](https://nominatim.org/)**: Free geocoding service

## 🎨 UI Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern Styling**: Custom CSS with gradients and animations
- **Interactive Elements**: Hover effects and smooth transitions
- **Autocomplete**: Smart city suggestions as you type
- **Example Questions**: Quick-start buttons for common queries

## 🚀 Deployment

### Streamlit Cloud
1. Push to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add your `OPENAI_API_KEY` in the secrets
4. Deploy!

### Docker (Optional)
```dockerfile
# Create a Dockerfile for containerized deployment
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000 8501
CMD ["python", "app.py"]
```

### Other Platforms
- **Heroku**: Use the provided `requirements.txt`
- **Railway**: Direct GitHub integration
- **Render**: Supports both frontend and backend
- **Vercel**: For static deployment (frontend only)

## 🛠️ Development

### Adding New Features
1. **New Weather Parameters**: Modify `weather_agent.py`
2. **UI Improvements**: Update `streamlit_app.py`
3. **API Enhancements**: Extend `app.py`

### Testing
```bash
# Test the FastAPI backend
curl -X POST "http://localhost:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "What is the weather in Paris?"}'
```

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

If you encounter any issues or have questions:
1. Check the [API documentation](http://localhost:8000/docs) when running
2. Ensure your OpenAI API key is valid
3. Verify all dependencies are installed correctly

---

**Made with ❤️ using Streamlit, FastAPI, and GPT-4**
