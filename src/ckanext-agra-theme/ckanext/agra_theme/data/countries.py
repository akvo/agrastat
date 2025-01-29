import requests

countries_data = requests.get(
    "https://gist.githubusercontent.com/almost/7748738/raw/575f851d945e2a9e6859fb2308e95a3697bea115/countries.json"
).json()
countries = [c["name"] for c in countries_data]
