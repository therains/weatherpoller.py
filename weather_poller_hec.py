import pandas as pd
import requests
import json
import urllib
import datetime


import requests
import json
import pandas as pd


#API Key
api_key = "423423no8a32valid423api6key"

# CSV file name
file_name = "fex_location_coords.csv"

configuration = {'splunk_collector_url':'-------',
                 'splunk_hec_token':'--------',
                 'splunk_sourcetype': '----------',
                 'splunk_index':''}


def get_weather_data(api_key: str, lat: float, lon: float) -> dict:
    weather_api = "https://api.openweathermap.org/data/2.5/weather?"
    response = requests.get(f"{weather_api}lat={lat}&lon={lon}&appid={api_key}&units=metric")
    return response.json()

def send_event_per_site(splunk_collector_url, splunk_hec_token, splunk_sourcetype, splunk_index, results):
    try:
        post_data = {
            "sourcetype": splunk_sourcetype,
            "event": json.dumps(results),
            "index": splunk_index
        }
        data = json.dumps(post_data).encode('utf8')
        auth_header = "Splunk %s" % splunk_hec_token
        headers = {'Authorization': auth_header}
        req = urllib.request.Request(splunk_collector_url, data, headers)
        response = urllib.request.urlopen(req)
        read_response = response.read()
        response_json = json.loads(str(read_response)[2:-1])
        if "text" in response_json and response_json["text"] == "Success":
            print("Event was recieved successfully")
        else:
            print("Error sending request.")
    except Exception as err:
        print("Error sending request")
        print(str(err))

        
def main (api_key: str, file_name: str, configuration: dict):
    df = pd.read_csv(file_name)
    for index, row in df.iterrows():
        site = row["site"]
        lat = row["lat"]
        lon = row["lon"]
        data = get_weather_data(api_key, lat, lon)
        results = {}
        results["time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        results[site] = data
        
        send_event_per_site(configuration['splunk_collector_url'], configuration['splunk_hec_token'], configuration['splunk_sourcetype'], configuration['splunk_index'], results)


results = main(api_key, file_name, configuration)

