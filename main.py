from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles  
import requests

# Create instance
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Tell FastAPI where to find the HTML templates (in the "templates" folder)
templates = Jinja2Templates(directory="templates")


# OpenWeatherMap API key (replace with your actual API key)
API_KEY = ""  # Replace with your OpenWeatherMap API key


# The root URL "/"
@app.get("/")
async def home(request: Request, city: str = "Tbilisi"):
    weather_data = fetch_weather(city)

    # Render the "index.html" template and pass weather data and city name
    return templates.TemplateResponse("index.html", {"request": request, "weather": weather_data, "city": city})


# Fetch weather data from the OpenWeatherMap API
def fetch_weather(city):
    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "clouds": data["clouds"]["all"]
        }
    else:
        print(f"Error: Received response status code {response.status_code}")
    return None