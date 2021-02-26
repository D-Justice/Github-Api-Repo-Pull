import requests
import re
import token_auth
import json
import time
pagenumber = 1

def userRepos():

    #prints out username, all public repository names and how many followers each one has
    global pagenumber
    repo = requests.get("https://api.github.com/users/{}/repos?page={}".format(user, pagenumber))
    rcount = 0
    count = 0
    pagenumber += 1
        
    print("\nDisplaying page {} of {}'s repositories".format(pagenumber, user))
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
                if item['name'] == "":
                    print("FUCKYES")
                    break
            except Exception as i:
                print(i)
    except:
        break#THIS IS THE KEY LINE (HOPEFULLY)
def userFollowers():
    global user
    global newusercount
    print("\nFollowers :\n")
    followers = requests.get("https://api.github.com/users/{}/followers".format(user))
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
user = input("Input GitHub User-name: ")
howmany = int(input("Enter how many additional users info you'd like to see:"))
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
rate = requests.get("https://api.github.com/rate_limit")
i = rate.json()['rate']['remaining']
repo = requests.get("https://api.github.com/users/{}/repos?page={}".format(user, pagenumber))
newusercount = 0
usernames = list()
jprint(i)
for i in range(howmany):
    while repo.status_code == 200:
        print(repo.status_code)
        if repo.status_code != 200:
            break
        else:
            userRepos()
    userFollowers()
        
#prints all of the user followers names, adds the first unique one it comes across to 'usernames'
#and then navigates to their page to repeat the proccess'
        
    


#jprint(followers.json())
#print(user)
print(usernames)
