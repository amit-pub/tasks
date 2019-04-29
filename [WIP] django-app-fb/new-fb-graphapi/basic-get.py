# source: https://django.cowhite.com/blog/understanding-facebook-graph-api-and-implementing-in-python-django/
import pdb

import requests
import urllib3

#facebook user access token

USER_ACCESS_TOKEN = 'EAAGICb3VPM8BAEzZCgPhvHygHl6ZAvjC1J0FdvZBXgiS5ra8F7SrsyoA0nmYvZC8xZBvATq1XsKpfxhr8qF4dpEGXAlzkkEauWDOBAOJOOHKgLTX4AxL8ig8dhBsE0uv9vMzVJiY6GwXUtphUHHJjfFzEDmgoPxcsvZCoGZCr45NiqEFcCyUWYhi2xOTJp2QmjvMZADiZBAmY9ZA4DcrJVtjAGcbWPnxS2ePAZD'


url = 'https://graph.facebook.com/me?fields=id,name'
#url = 'https://graph.facebook.com/

parameters = {'access_token': USER_ACCESS_TOKEN}

resp = requests.get(url, params=parameters)
pdb.set_trace()
