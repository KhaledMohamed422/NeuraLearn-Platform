import requests
from decouple import config


url = config("TRANSCRIPT_MODEL_URL")
headers = {"Authorization": f"Bearer {config("TRANSCRIPT_TOKEN")}"}

filename= input("Enter The full path of audio file: ")
with open(filename, "rb") as f:
    data = f.read()
r = requests.post(url, headers=headers, data=data)
print(r.json())