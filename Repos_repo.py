import requests
import re
import json
user = input("Input GitHub User-name: ")



repo = requests.get("https://api.github.com/users/{}/repos".format(user))
rate = requests.get("https://api.github.com/rate_limit")
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

for item in repo.json():
    try:
        print(item['name'])
    except Exception as i:
        print(i)


jprint(rate.json()['rate']['remaining'])