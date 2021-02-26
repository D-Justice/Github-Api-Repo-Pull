import requests
import re
import token_auth
import json
import time

user = input("Input GitHub User-name: ")
howmany = int(input("Enter how many additional users info you'd like to see:"))
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
rate = requests.get("https://api.github.com/rate_limit")
i = rate.json()['rate']['remaining']

usernames = list()

for i in range(howmany):
    repo = requests.get("https://api.github.com/users/{}/repos".format(user))
    followers = requests.get("https://api.github.com/users/{}/followers".format(user))
    rcount = 0
    count = 0
#prints out username, all public repository names and how many followers each one has
    try:
        for item in repo.json():
            newusercount = 0
            if count >= 1:pass
            else: 
                count += 1
                print('\nUsername:',item['owner']['login'],"\n\n") 
            try:
                rcount += 1
                print(('Repo #{}:').format(rcount),item['name'],'has------',item['watchers'],'watchers')
            
            except Exception as i:
                print(i)
        print("\nFollowers :\n")
#prints all of the user followers names, adds the first unique one it comes across to 'usernames'
#and then navigates to their page to repeat the proccess'
        for users in followers.json():
            try:
                print(users['login'])
            except:
                continue


            if users['login'] not in usernames:
                if newusercount == 0:
                    newusercount += 1
                    usernames.append(user)
                    user = users['login']
                    
            else:
                continue


    except Exception as error:
        print("ERROR: Please enter a valid username :")
        print(error)
        quit()
#jprint(followers.json())
#print(user)
print(usernames)
jprint(i)