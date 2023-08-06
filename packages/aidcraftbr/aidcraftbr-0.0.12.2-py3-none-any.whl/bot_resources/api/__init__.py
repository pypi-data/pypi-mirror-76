import requests

def send(unprodata, url):
  url = "http://www.example.com/page"

  req = request.post(url=url, data=unprodata)
  response = request.urlopen(req)

  return response.text