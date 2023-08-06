import requests

def send(unprodata, url):

  req = requests.post(url=url, data=unprodata)
  response = requests.urlopen(req)

  return response.text