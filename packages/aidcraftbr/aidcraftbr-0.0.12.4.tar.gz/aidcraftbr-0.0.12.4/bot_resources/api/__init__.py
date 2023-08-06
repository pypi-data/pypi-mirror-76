import requests

def send(unprodata, url):

  req = requests.post(url=url, data=unprodata)
  response = request.urlopen(req)

  return response.text