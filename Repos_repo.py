import requests
import token_auth
import re
import json
user = input("Input GitHub User-name: ")



token = token_auth.token
repo = requests.get("https://api.github.com/users/{}/repos".format(user))
rate = requests.get("https://api.github.com/rate_limit")
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

result = json.dumps(repo.json())
result = result.split()
string = ""
for item in result:
    string += item
find = re.findall('"name":"[^\"]+', string)
#print(string)

for i in find:
    print(i.title().replace('"', ""))



jprint(rate.json()['rate']['remaining'])