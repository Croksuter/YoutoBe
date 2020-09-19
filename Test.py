import requests
import time
import pytube

key = ""
url = "https://www.googleapis.com/youtube/v3/video"

response = requests.get("https://www.googleapis.com/youtube/v3/videos",
                                params={"part": "contentDetails",
                                        "key": key,
                                        "id": "I3kd3M2IRu4"})

data = response.json()
print(data)
