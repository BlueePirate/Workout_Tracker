import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
import os

NUTRITION_API = os.environ["nutrition_api"]
ACCOUNT_ID = os.environ["account_id"]
EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

SHEETY_ENDPOINT = os.environ["SHEETY_ENDPOINT"]

BASIC_AUTH_PASSWORD = os.environ["BASIC_AUTH_PASSWORD"]

headers = {
    "x-app-id": ACCOUNT_ID,
    "x-app-key": NUTRITION_API,
}

query = input("what exercise have you done today? ")
gender = input("what is your gender, Male or Female? ")
age = int(input("How old are you? "))
weight = int(input("HOw much do you weigh? In kgs! "))
height = int(input("How tall are you? In cm! "))

params = {
    "query": query,
    "gender": gender,
    "weight_kg": weight,
    "height_cm": height,
    "age": age,
}

response = requests.post(url=EXERCISE_ENDPOINT, json=params, headers=headers)
data = response.json()
print(data)


today = datetime.now().strftime("%d/%m/%Y")
time = datetime.now().strftime("%X")

basic = HTTPBasicAuth('gunaraj', password=BASIC_AUTH_PASSWORD)

for exercise in data["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today,
            "time": time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    result = requests.post(url=SHEETY_ENDPOINT, json=sheet_inputs, auth=basic)
    print(result.text)
