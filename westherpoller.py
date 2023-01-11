import requests
import json
import csv

def get_weather(api_key, lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = json.loads(response.text)
        return data
    except requests.exceptions.HTTPError as errh:
        print ("HTTP Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("Something went wrong, please check your connection",err)
    return None

def save_weather_to_json(data, hostname, lat, lon):
    if data is not None:
        filename = f"{hostname}_weather_{lat}_{lon}.json"
        with open(filename, 'w') as f:
            json.dump(data, f)
        print(f"Weather data for {lat}, {lon} saved to {filename}")
    else:
        print(f"Failed to get weather data for {lat}, {lon}")

def get_locations_from_csv(file_path):
    locations = []
    try:
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # skip the header row
            for row in reader:
                lat = float(row[0])
                lon = float(row[1])
                hostname = row[2]
                locations.append((lat, lon, hostname))
        return locations
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def get_weather_for_locations(api_key, locations):
    if locations is not None:
        for lat, lon, hostname in locations:
            data = get_weather(api_key, lat, lon)
            save_weather_to_json(data, hostname, lat, lon)
    else:
        print("No location data found.")

def __main__():
    api_key = "YOUR_API_KEY_HERE"
    file_path = 'locations.csv'
    locations = get_locations_from_csv(file_path)
    get_weather_for_locations(api_key, locations)

if __name__ == '__main__':
    __main__()
