from jotform import *
import requests

api_key = '9b23a50e2f6edfa7a379120cbc3ecc1e'

r = requests.get("https://api.jotform.com/user/submissions", params={"apiKey" : api_key})

print r.text


# client = JotformAPIClient('9b23a50e2f6edfa7a379120cbc3ecc1e', debug=True)

#form = client.get_form('41834215201341')

#print form