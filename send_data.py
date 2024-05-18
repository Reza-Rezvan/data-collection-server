import json
import time
import random
import requests
from datetime import datetime
import os
import base64

# Define the path to the images directory
image_dir = r'your path'

# create random data, you can create ant random data like this base on your database.db tabels
def create_random_data_with_image(image_path):
    hardware_id = random.randint(1, 2)
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%Y-%m-%d")
    speed = random.uniform(0, 120)
    label = random.choice(['distract', 'Notdistract'])
    
    # encode image
    with open(image_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
    
    return {
        "hardware_id": hardware_id,
        "timestamp": {
            "time": time_str,
            "date": date_str
        },
        "speed": speed,
        "label": label,
        "image_data": image_data
    }

# your server url
def send_data_to_server(data):
    url = 'http://your ip:your port/upload'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=data, timeout=30)  # Increase timeout to 30 seconds
    return response.json()

if __name__ == "__main__":
    image_files = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
    end_time = time.time() + 20
    while time.time() < end_time:
        for image_path in image_files:
            data = create_random_data_with_image(image_path)
            try:
                response = send_data_to_server(data)
                print(response)
            except requests.exceptions.Timeout:
                print(f"Request timed out for image {image_path}")
            except requests.exceptions.ConnectionError as e:
                print(f"Connection error for image {image_path}: {e}")
            time.sleep(5)
