import requests
import re
import json
import time
pagenumber = 1
totalcount = 0
def userRepos():

    #prints out username, all public repository names and how many followers each one has
    global pagenumber
    global totalcount
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
                totalcount += 1
                print(('Repo #{}:').format(totalcount),item['name'],'has------',item['watchers'],'watchers')
            except Exception as i:
                print(i)
    except:
        print('Failed')
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

usernames = list()
jprint(i)
howmany = (howmany * 2) + 1
def totalRepoUser():
    totalRepo = requests.get("https://api.github.com/users/{}".format(user))
    global totalRepoNumber
    totalRepoNumber = totalRepo.json()['public_repos']

    print(totalRepoNumber)
for i in range(howmany):
    totalRepoUser()
    print(i)
    newusercount = 0
    pagenumber = 1
    if totalcount == totalRepoNumber:
        userFollowers()
        totalcount = 0

    else:
        while totalcount < totalRepoNumber:
            userRepos()
            print(totalcount, totalRepoNumber)

#prints all of the user followers names, adds the first unique one it comes across to 'usernames'
#and then navigates to their page to repeat the proccess'




#jprint(followers.json())
#print(user)
print(usernames)
