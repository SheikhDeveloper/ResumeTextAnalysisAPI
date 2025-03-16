import requests
import time

URL = 'localhost:5000/resume_analysis/predict'

while True:
    resp = requests.get(URL)
    time.sleep(300)
