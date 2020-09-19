from youtubesearchpython import SearchVideos
import json
search = SearchVideos("24시간동안 라이더하기", offset = 1, mode = "json", max_results = 20)

print(json.loads(search.result())['search_result'])