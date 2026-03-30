import urllib.request
url = 'https://web.archive.org/web/20120220191837id_/http://linux01.gwdg.de/~alatham/stego/jphswin_05.zip'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
res = urllib.request.urlopen(req).read()
with open('jphs_raw.zip', 'wb') as f:
    f.write(res)
