import requests
import json

# La tua chiave API di WeatherAPI.com
api_key = 'baa67000bbc64e51a30100644252401'

# Lista delle località di interesse
locations = [
    'Catania', 'Acireale', 'Misterbianco', 'Paternò', 'Gravina di Catania', 
    'Mascalucia', 'Adrano', 'Nicolosi', 'Aci Castello'
]

# Funzione per ottenere e inviare le informazioni meteorologiche a Logstash
def get_weather(location):
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&lang=it'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Solleva un'eccezione per errori HTTP
        data = response.json()
        
        # Invia i dati a Logstash
        logstash_url = "http://localhost:5044"
        headers = {"Content-Type": "application/json"}
        payload = {
            "location": data['location']['name'],
            "temperature": data['current']['temp_c'],
            "condition": data['current']['condition']['text'],
            "wind_kph": data['current']['wind_kph'],
            "wind_dir": data['current']['wind_dir'],
            "pressure_mb": data['current']['pressure_mb'],
            "humidity": data['current']['humidity'],
            "cloud": data['current']['cloud'],
            "feelslike_c": data['current']['feelslike_c'],
            "visibility_km": data['current']['vis_km']
        }
        logstash_response = requests.post(logstash_url, data=json.dumps(payload), headers=headers)
        logstash_response.raise_for_status()
        print(f"Dati inviati a Logstash per {location}")

    except requests.exceptions.HTTPError as http_err:
        print(f"Errore HTTP per {location}: {http_err}")
    except Exception as err:
        print(f"Errore per {location}: {err}")

# Itera su ciascuna località e ottiene le informazioni meteorologiche
for location in locations:
    get_weather(location)