import requests
import re
import json
import sqlite3
import time
#Creates .sqlite tables  
conn = sqlite3.connect('GitHubUserData.sqlite')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS GitHubData
            (ID INTEGER, User TEXT, Repositories INTEGER, Followers INTEGER)''')
cur.execute('''CREATE TABLE IF NOT EXISTS GitHubUserInfo
            (ID INTEGER, User TEXT, Repos_Number INTEGER, Repositories TEXT, Followers TEXT)''')
#Increments to work through all page numbers
pagenumber = 0
#Counts every repository that is printed out and displays its number
totalcount = 0
#Increments by one through each full iteration to provide the 'ID' column in database
id = 0

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
        #Runs through each repository on a page and prints it and how many followers it has
        for item in repo.json():
            newusercount = 0
            global usersName
            usersName = item['owner']['login']
           
            if count >= 1:pass
            else:
                count += 1
                print('\nUsername:', usersName,"\n\n")
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
def waitPeriod():
    print("Taking a break")
    ratecount = 0
    time.sleep(5)
    print("Please wait 1 hour before continuing")
    time.sleep(905)
    print("25% there!")
    time.sleep(905)
    print("Halfway there!")
    time.sleep(905)
    print("75% there!")
    time.sleep(905)
    print("Done!")
    endnowcount += 1
    if endnowcount == 5:
        print("List of all unique usernames: \n", usernames)
        endnowcount = 0
def lookForward():
    totalRepo = requests.get("https://api.github.com/users/{}".format(user))
    totalRepoNumber = totalRepo.json()['public_repos']
    pages = float(totalRepoNumber / 30)
    pages = rateLeft - pages 
    print(pages)
    if pages <= 0:
        print("Only {} left, pausing".format(round(pages, 0)))
        waitPeriod()
    else:
        print("Rate left sufficient. {} extra".format(round(pages, 0)))
        pass
user = input("Input GitHub User-name: ")
howmany = int(input("Enter how many additional users info you'd like to see:"))
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
rate = requests.get("https://api.github.com/rate_limit")
rateLeft = rate.json()['rate']['remaining']

repo = requests.get("https://api.github.com/users/{}/repos?page={}".format(user, pagenumber))
ratecount = 0
usernames = list()
testcount = 0
endnowcount = 0
howmany = (howmany * 2) + 1
def totalRepoUser():
    totalRepo = requests.get("https://api.github.com/users/{}".format(user))
    global totalRepoNumber
    global endnowcount
    global numOfFollowers
    totalRepoNumber = totalRepo.json()['public_repos']

    numOfFollowers = totalRepo.json()['followers']

    print(totalRepoNumber)
for i in range(howmany):
    lookForward()
    totalRepoUser()
    ratecount += 1
    print(i)
    newusercount = 0
    print(ratecount)
    pagenumber = 1
    if ratecount > 35:
        waitPeriod()
    elif totalcount == totalRepoNumber:
        userFollowers()
        ratecount += 1
        totalcount = 0
        id += 1
        print("RateCount: ", ratecount, "\nRateLeft: ", rateLeft, "\nTestCount: ", testcount)
        cur.execute('''INSERT OR REPLACE INTO GitHubData(ID, User, Repositories, Followers)
                    VALUES (?, ?, ?, ?)''', (id, usersName, totalRepoNumber, numOfFollowers))
        conn.commit()
    else:
        while totalcount < totalRepoNumber:
            userRepos()
            ratecount += 1
            print("Printing: ",totalcount, "out of: ", totalRepoNumber,"\nRateCount: ", ratecount,"\nRateLeft: ", rateLeft, "\nTestCount: ", testcount)     

#prints all of the user followers names, adds the first unique one it comes across to 'usernames'
#and then navigates to their page to repeat the proccess'




#jprint(followers.json())
#print(user)
print(usernames)
