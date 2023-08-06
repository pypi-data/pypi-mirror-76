import requests

def send(unprodata, url):

  req = request.post(url=url, data=unprodata)
  response = request.urlopen(req)

  return response.text