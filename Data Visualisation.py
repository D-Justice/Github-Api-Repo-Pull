import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
con = sqlite3.connect("GitHubUserData.sqlite")
df =pd.read_sql_query("SELECT * from GitHubData", con)


Repos = df.plot(y='Repositories')
plt.show()

con.close()