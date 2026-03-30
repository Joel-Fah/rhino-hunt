import urllib.request
import json
try:
    url = "https://api.github.com/search/repositories?q=jphide"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urllib.request.urlopen(req).read()
    data = json.loads(res.decode('utf-8'))
    print("Found items:")
    for item in data.get('items', []):
        print(item['html_url'])
except Exception as e:
    print(e)
