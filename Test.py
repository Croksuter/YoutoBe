import requests
import time
import pytube

key = ""
url = "https://www.googleapis.com/youtube/v3/search"

params = {"q": "망상감상대상연맹",
          "part": "snippet",
          "key": key,
          "maxResult": 5}
response = requests.get(url, params=params)

data = response.json()
queue_data = []
start = time.time()
for i in data['items']:
    queue_data.append((i['snippet']['title'], i['id']['videoId']))
print(time.time()-start)
print(queue_data)
length_data = []
start = time.time()
for i in queue_data:
    length_data.append(pytube.YouTube('https://www.youtube.com/watch?v='+i[1]).length)
print(time.time()-start)
print(length_data)
