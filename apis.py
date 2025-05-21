import requests
import os
from dotenv import load_dotenv
import random

def get_random_dog_image(): 
    load_dotenv()
    token = os.environ['PEXELS_API_KEY']
    page = random.randint(1, 1000)
    query = "cute animals"

    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1&page={page}"
    headers = {
        "Authorization": f"{token}",  # Pexels NO requiere "Bearer", solo el token
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    image_url = data['photos'][0]['src']['original']
    return image_url
    


def get_motivational_quote():
    response = requests.get("https://zenquotes.io/api/random")
    data = response.json()
    return f"{data[0]['q']} — {data[0]['a']}. Follow for daily cute animals pics and motivational quotes #CuteAnimalsDaily #DailyMotivation"


