import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import style
con = sqlite3.connect("GitHubUserData.sqlite")
cur = con.cursor()
cur.execute('SELECT Repositories, Followers FROM GitHubData')

data = cur.fetchall()

Repositories = []
Followers = []
averageRepos = []
averageFollowers = []
count = 0
reposTotal = 0
for row in data:
    if row[1] >= 9999999:
        continue
    else:
        if row[0] >= 999999:
            continue
        else:
            Repositories.append(row[0])
            averageRepos.append(row[0])
            Followers.append(row[1])
            averageFollowers.append(row[1])
            count += 1
#print(Repositories, Followers)
for average in averageRepos:
    reposTotal += average
followersTotal = 0
for average in averageFollowers:
    followersTotal += average
averageFollowers = followersTotal / count
averageRepos = reposTotal / count

print("Average amount of repos is {}".format(int(averageRepos)))
print("Average amount of followers is {}".format(int(averageFollowers)))
sns.regplot(x=Repositories, y=Followers, line_kws={"color":"r","alpha":0.7,"lw":2})
plt.xlabel("Repositories")
plt.ylabel("Followers")
plt.show()
con.close()