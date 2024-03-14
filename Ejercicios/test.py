import requests
url = "https://api.met.no/weatherapi/locationforecast/2.0/compact.json"
params = {'lat':'19.42847','lon':'-99.12766'}
payload = {}
headers = {}
response = requests.request("GET", url, headers=headers, data=payload, params=params, timeout=10)

print(response.text)