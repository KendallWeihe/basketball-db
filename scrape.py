import requests
from bs4 import BeautifulSoup
import pdb
import numpy as np
import re
import os

website = "http://www.sports-reference.com"
dayLink = "/cbb/boxscores/index.cgi?month=03&day=07&year=2017"
year = "2017"

while 1:
    print dayLink
    r = requests.get(website+dayLink)
    outerSoup = BeautifulSoup(r.text, "html.parser")
    teams = outerSoup.findAll('table', class_='teams')
    boxScores = outerSoup.findAll('a', href=True, text='Final')
    for i in range(len(boxScores)):
        try:
            gameLink = str(boxScores[i]['href'])
            r = requests.get(website+gameLink)
            soup = BeautifulSoup(r.text, "html.parser")

            tr1 = soup.findAll('tr', class_='thead')[1].findAll('td')
            tr2 = soup.findAll('tr', class_='thead')[3].findAll('td')

            team1_stats_today = []
            team2_stats_today = []
            for j in range(1, len(tr1)):
                team1_stats_today.append(float(tr1[j].string))
                team2_stats_today.append(float(tr2[j].string))

            score1 = float(soup.findAll('div', class_='score')[0].string)
            score2 = float(soup.findAll('div', class_='score')[1].string)
            spread = score1 - score2

            team1_out = team1_stats_today + team2_stats_today + [score1, score2, spread]
            team2_out = team2_stats_today + team1_stats_today + [score1, score2, spread]

            team1 = str(teams[i].findAll('a')[0].string).replace(" ", "-").replace("\'", "")
            team2 = str(teams[i].findAll('a')[2].string).replace(" ", "-").replace("\'", "")

            try:
                team1_stats = np.genfromtxt("./seasons/"+year+"/"+team1+".csv", delimiter=",")
                team2_stats = np.genfromtxt("./seasons/"+year+"/"+team2+".csv", delimiter=",")

                team1_stats = np.vstack((team1_stats, team1_out))
                team2_stats = np.vstack((team2_stats, team2_out))
            except:
                team1_stats = np.array([team1_out])
                team2_stats = np.array([team2_out])

            np.savetxt("./seasons/"+year+"/"+team1+".csv", team1_stats, delimiter=",")
            np.savetxt("./seasons/"+year+"/"+team2+".csv", team2_stats, delimiter=",")

        except:
            pass

    dayLink = str(outerSoup.findAll('a', class_='button2')[0]['href'])
    date = str(soup.findAll('a', class_='button2')[0].string)
    if re.findall("October", date):
        year = str(int(year)-1)
        os.mkdir("./seasons/"+year)
