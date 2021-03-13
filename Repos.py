import requests
import re
import json
import sqlite3
import time
import random
from datetime import datetime, timedelta
#Creates .sqlite tables  
conn = sqlite3.connect('GitHubUserData.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS GitHubUserInfo
            (ID INTEGER, User TEXT, Repos_Number INTEGER, Repositories TEXT, Followers TEXT)''')
#Increments to work through all page numbers
pagenumber = 1
#Counts every repository that is printed out and displays its number
totalcount = 0
#Increments by one through each full iteration to provide the 'ID' column in database
id = 0
largestFollowers = 0
largestFollowersUser = None
usernames = list()
textFile = open('list_storage.txt', 'r')
for line in textFile:
    splitUserNames = line.split()
    for single in splitUserNames:
        cleaned = single.replace("'","")
        cleaned = cleaned.replace(",","")
        cleaned = cleaned.replace("[","")
        cleaned = cleaned.replace("]","")
        usernames.append(cleaned)
print(usernames)
def userRepos():

    #prints out username, all public repository names and how many followers each one has
    global pagenumber
    global totalcount
    repo = requests.get("https://api.github.com/users/{}/repos?page={}".format(user, pagenumber))
    
    #Makes sure to only append first unique name to UserNames list
    uniqueUser = 0
    pagenumber += 1

    print("\nDisplaying page {} of {}'s repositories".format(pagenumber, user))
    try:
        #Runs through each repository on a page and prints it and how many followers it has
        for item in repo.json():
            newusercount = 0
            global usersName
            usersName = item['owner']['login']
           
            if uniqueUser >= 1:pass
            else:
                uniqueUser += 1
                
                print('\nUsername:', usersName,"\n\n")

            try:
                totalcount += 1
                print(('Repo #{}:').format(totalcount),item['name'],'has------',item['watchers'],'watchers')

            except Exception as i:
                print(i)
    except:
        print('Failed')
#Grabs first page of users followers and prints it out, grabs first unique name to run through on next iteration
def userFollowers():
    global largestFollowers
    global largestFollowersUser
    global user
    global newusercount
    print("\n{} has {} followers :\n".format(user,numOfFollowers))
    followers = requests.get("https://api.github.com/users/{}/followers".format(user))
    for users in followers.json():
        try:
            print(users['login'])
        except:
            continue

        #Adds unique username to usernames list
        if users['login'] not in usernames:
            print("This persons number of followers is {}".format(numOfFollowers))
            print(type(numOfFollowers))
            infoFollowers = users['login']
            totalRepo = requests.get("https://api.github.com/users/{}".format(infoFollowers))
            try:
                if numOfFollowers >= largestFollowers:
                    largestFollowers = numOfFollowers
                    largestFollowersUser = users['login']
                    try:
                        largestUserMemory = open('large_user.txt','r')
                    except:
                        print("large_user.txt not found: creating")
                        largestUserMemory = open('large_user.txt', 'w')
                        largestUserMemory.write("NoUser 000")
                        largestUserMemory.close()
                        largestUserMemory = open('large_user.txt','r')
                        
                    for line in largestUserMemory:
                        followerNumber = line.split()
                        followerNumber = followerNumber[1]
                        followerNumber = int(followerNumber)
                        try:
                            if followerNumber <= largestFollowers:
                                largestUserMemory = open('large_user.txt','w')
                                largestUserMemory.write(largestFollowersUser)
                                largestUserMemory.write(largestFollowers)
                            else:
                                print("User is smaller than previous largest")
                        except:
                            print("None found")
                    
                    print("The current largest is:",largestFollowersUser, largestFollowers)
                else:
                    print("Not large enough")
                
                if numOfFollowers <= 10:
                    print("=====NOT ENOUGH FOLLOWERS====")
                    user = None
                    
                elif numOfFollowers >= 11:
                    if newusercount == 0:
                        newusercount += 1
                        usernames.append(user)
                        user = users['login']
                        
                    else:
                        continue
                else:
                    print("not working")
            except Exception as i:
                print("Not working cos",i)
        else:
            continue
        if user == None:
            print("No viable users found, using {} who had {} followers".format(largestFollowersUser, largestFollowers))
        else:
            continue
#Pauses program for 1 hour when rate limit is nearly used up
def waitPeriod():
    global endnowcount
    global largestFollowers
    global largestFollowersUser
    print("Our top contender is {} with {} followers".format(largestFollowersUser, largestFollowers))
    dateTime = open('dateTime.txt', 'r')
    lines = str(dateTime.readlines())
    time1 = lines[13:18]
    time2 = lines[45:50]
    print("Process began at {}, expect the next iteration to begin sometime before {}".format(time1,time2))
    dateTime.close()
    #Only adds new usernames to text file
    textFile = open('list_storage.txt', 'w')
    textFile.write(" {}".format(str(usernames)))
    textFile.close()
    print("Saving unique usernames to 'list_storage.txt'")
    
    ratecount = 0
    limitReached = True
    firstIteration = True
    while limitReached:
        rate = requests.get("https://api.github.com/rate_limit")
        rateLeft = rate.json()['rate']['remaining']
        randoChoice = ["\nShouldn't be TOO much longer... Just a sec...", 
        "\nStill looking for more api access? Greedy...",
        "\nStill waiting? Read the first message again","\nThis will be the time! Any second now...",
        "\nI swear I'm actually doing something to fix this","\nYou try counting to 600 multiple times with no break, see how YOU like it?",
        "\nPlease wait.. Deleting SYS32~"]
        
        if firstIteration == True:
            print("\nRate limit reached, trying again in a few minutes")
            firstIteration = False
        else:
            print(random.choice(randoChoice))
        time.sleep(180)
        
        try:
            if rateLeft >= 40:
                print('Success')
                limitReached = False
                pass
            else:
                print('Continuing')
                continue
        except Exception as i:
            print('Not working cos',i)
    print("Done!")
    endnowcount += 1
    ratecount = 0
    dateTime = open('dateTime.txt', 'w')
    dateTime.write(str(datetime.now()))
    fromNow = (datetime.now() + timedelta(hours= 1))
    dateTime.write("\n{}".format(str(fromNow)))
    dateTime.close()
def hyperDataGather():
    newusercount = 0
    global user
    global totalRepoNumber
    global numOfFollowers
    followers = requests.get("https://api.github.com/users/{}/followers".format(user))
    totalRepo = requests.get("https://api.github.com/users/{}".format(user))
    totalRepoNumber = totalRepo.json()['public_repos']
    numOfFollowers = totalRepo.json()['followers']
    for i in followers.json():
        if i['login'] not in usernames:
            if newusercount == 0:
                newusercount += 1
                usernames.append(user)
                user = i['login']
                usersName = user
                followers = requests.get("https://api.github.com/users/{}/followers".format(user))
                numOfFollowers = totalRepo.json()['followers']
                print(numOfFollowers)
                if numOfFollowers <= 0:
                    print('Low followers')
                    
                    continue
                
                print("Found user: {}".format(user))
                
                
            else:
                continue
        else:
            continue
            
    
#Looks at how many repository pages there are to make sure rate limit is sufficient
def lookForward():
    global rateLeft
    totalRepo = requests.get("https://api.github.com/users/{}".format(user))
    rate = requests.get("https://api.github.com/rate_limit")
    totalRepoNumber = totalRepo.json()['public_repos']
    rateLeft = rate.json()['rate']['remaining']
    pages = int(totalRepoNumber / 30)
    pages = rateLeft - pages 
    if pages <= 1:
        print("Only {} left, pausing".format(pages))
        waitPeriod()
    else:
        print("Rate left sufficient. {} extra".format(pages))
        pass
user = input("Input GitHub User-name: ")
if user.lower() == "rate":
    rate = requests.get("https://api.github.com/rate_limit")
    rateLeft = rate.json()['rate']['remaining']
    print(rateLeft)
    quit()
howmany = int(input("Enter how many additional users info you'd like to see:"))
#Prints json data in a pretty way
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

firstIteration = True
repo = requests.get("https://api.github.com/users/{}/repos?page={}".format(user, pagenumber))
#Keeps count of the rates used up
ratecount = 0

#prints out list of unique usernames every 5 pauses
endnowcount = 0
#Times howmany by two because repositories and followers are two different itterations
howmany = (howmany * 2) + 1
#Records how many total repositories the user has
def totalRepoUser():
    totalRepo = requests.get("https://api.github.com/users/{}".format(user))
    global totalRepoNumber
    global endnowcount
    global numOfFollowers
    totalRepoNumber = totalRepo.json()['public_repos']

    numOfFollowers = totalRepo.json()['followers']

    print(totalRepoNumber)
#Runs through each unique users repositories and followers and records number of repositories and followers into a DB 
for i in range(howmany):
    if firstIteration == True:
        dateTime = open('dateTime.txt', 'w')
        dateTime.write(str(datetime.now()))
        fromNow = (datetime.now() + timedelta(hours= 1))
        dateTime.write("\n{}".format(str(fromNow)))
        dateTime.close()
        firstIteration = False
    #try:
        #lookForward()
    #except:
        #waitPeriod()
    #totalRepoUser()
    #ratecount += 1
    #newusercount = 0
    #pagenumber = 1
    #if totalcount == totalRepoNumber:
        #userFollowers()
        #ratecount += 1
        #totalcount = 0
    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS GitHubData
            (ID INTEGER, User TEXT, Repositories INTEGER, Followers INTEGER)''')
        hyperDataGather()
        id += 1
        #print("Rate Count: ", ratecount, "\nRate Left: ", rateLeft)
        cur.execute('''INSERT OR REPLACE INTO GitHubData(ID, User, Repositories, Followers)
        VALUES (?, ?, ?, ?)''', (id, user, totalRepoNumber, numOfFollowers))
        conn.commit()
        print('Committed {}'.format(user))
    except Exception as i:
        print(i)
        conn.close()
        waitPeriod()
    #else:
        #while totalcount < totalRepoNumber:
            #lookForward()
            #userRepos()
            #ratecount += 1
            #print("Printing: ",totalcount, "out of: ", totalRepoNumber,"\nRateCount: ", ratecount,"\nRateLeft: ", rateLeft)     


print(usernames)
