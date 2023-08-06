import requests

def send(unprodata, url):

  req = requests.post(url=url, data=unprodata)

  return req.text