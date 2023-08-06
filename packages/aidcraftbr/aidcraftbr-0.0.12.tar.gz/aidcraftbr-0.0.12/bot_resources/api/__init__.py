from urllib import request, parse

def send(unprodata, url):
  url = "http://www.example.com/page"
  data = parse.urlencode(unprodata).encode()

  req = request.Request(url, data=data)
  response = request.urlopen(req)

  print (response.read())