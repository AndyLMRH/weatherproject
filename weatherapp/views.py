from django.shortcuts import render
from django.conf import settings
import requests
import datetime

def home(request):
    city = request.GET.get("city", "Oshawa")
    country = request.GET.get("country", "CA")

    # Weather API
    WEATHER_API_KEY = settings.OPENWEATHER_API_KEY
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={WEATHER_API_KEY}'
    PARAMS = {'units': 'metric'}

    # Google Custom Search
    API_KEY = settings.GOOGLE_CSE_API_KEY
    SEARCH_ENGINE_ID = settings.GOOGLE_CSE_ID

    query = f"{city} {country}"  # Add space for relevance
    city_url = (
    f"https://www.googleapis.com/customsearch/v1?"
    f"key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&searchType=image&num=1"
)


    # Fetch Google image safely
    image_url = None
    try:
        img_data = requests.get(city_url).json()
        search_items = img_data.get("items")
        if search_items:
            image_url = search_items[0]['link']
    except Exception as e:
        print("Google image search failed:", e)
        image_url = None


    # Fetch weather safely
    try:
        data = requests.get(url, params=PARAMS).json()
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        day = datetime.date.today()
        exception_occurred = False
    except Exception as e:
        print("Weather API failed:", e)
        description = "clear sky"
        icon = "01d"
        temp = 25
        day = datetime.date.today()
        exception_occurred = True
    
    return render(request, 'weatherapp/index.html', {
        "description": description,
        "icon": icon,
        "temp": temp,
        "day": day,
        "city": city if not exception_occurred else "indoors",
        "exception_occurred": exception_occurred,
        "image_url": image_url
    })
