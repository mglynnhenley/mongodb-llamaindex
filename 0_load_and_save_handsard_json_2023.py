import requests
import os
import json
from datetime import datetime, timedelta

def get_debates_for_date(date, api_key):
    base_url = "https://www.theyworkforyou.com/api/getDebates"
    params = {
        "type": "commons",  # Adjust as needed
        "date": date,
        "key": api_key,
        "output": "js"  # Assuming JSON format is still what we want
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()  # Directly return the JSON without converting to string
    else:
        print(f"Error fetching data for {date}: {response.status_code}")
        return None

def save_to_json_file(directory, date, data):
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, f"{date}.json")  # Save as .json
    with open(file_path, "w") as file:  # Use 'w' to write JSON data
        json.dump(data, file, ensure_ascii=False, indent=4)  # Properly format JSON

def main():
    start_date = datetime(year=2023, month=1, day=1)
    end_date = datetime(year=2023, month=12, day=31)
    api_key = "Gn9xyaAiFPpVBe6rMjA6grpf"  # Replace with your actual API key
    directory = "hansard-2023"
    
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        debates = get_debates_for_date(date_str, api_key)
        if debates is not None:
            save_to_json_file(directory, date_str, debates)  # Save directly as JSON
        current_date += timedelta(days=1)

if __name__ == "__main__":
    main()
