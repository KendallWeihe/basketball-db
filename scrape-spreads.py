import requests
from bs4 import BeautifulSoup
import pdb
import difflib
import numpy as np

teamsFile = open("./teams.txt", "r")
teams = teamsFile.read().splitlines()

link = "https://www.teamrankings.com/ncb/schedules/?date="
links = []
# for i in range(1,19):
#     links.append(link+'{:02}'.format(i))

for i in range(2011,2018):
    links = []
    year = i
    for j in range(11,13):
        for k in range(1,31):
            links.append("{}{}-{}-{}".format(link, year, str(j).zfill(2), str(k).zfill(2)))
    year = year + 1
    for j in range(1,5):
        for k in range(1,29):
            links.append("{}{}-{}-{}".format(link, year, str(j).zfill(2), str(k).zfill(2)))

    aggregate_data = []
    for l in links:
        print l
        try:
            r = requests.get(l)
            soup = BeautifulSoup(r.text, "html.parser")

            date = l[l.index("=")+1:l.index("=")+5] + l[l.index("=")+6:l.index("=")+8] + l[l.index("=")+9:l.index("=")+11]

            games = soup.find("table", class_="tr-table datatable scrollable")
            game_links = games.findAll("a")
        except:
            continue

        for game in game_links:
            try:
                game_link = "https://www.teamrankings.com" + str(game["href"])
                print game_link
                r = requests.get(game_link)
                inner_soup = BeautifulSoup(r.text, "html.parser")

                team1_name = str(inner_soup.findAll('h1')[0].findAll('a')[0].string).strip()
                team2_name = str(inner_soup.findAll('h1')[0].findAll('a')[1].string).strip()

                try:
                    team1_name_in_teams = difflib.get_close_matches(team1_name, teams, n=1)[0]
                    team2_name_in_teams = difflib.get_close_matches(team2_name, teams, n=1)[0]
                    team1_index = teams.index(team1_name_in_teams)
                    team2_index = teams.index(team2_name_in_teams)
                except:
                    continue

                table = inner_soup.findAll("table", class_="tr-table matchup-table")[4]
                data = table.findAll("td")

                team1_vegas_score = str(data[2].string)
                team2_vegas_score = str(data[6].string)

                team1_score = str(data[3].string)
                team2_score = str(data[7].string)

                spread1 = str(int(team1_score) - int(team2_score))
                spread2 = str(int(team2_score) - int(team1_score))

                team1_data = [int(date), int(team1_index), int(team2_index), float(team1_vegas_score), \
                        float(team2_vegas_score), int(team1_score), int(team2_score), int(spread1)]

                team2_data = [int(date), int(team2_index), int(team1_index), float(team2_vegas_score), \
                        float(team1_vegas_score), int(team2_score), int(team1_score), int(spread2)]

                aggregate_data.append(team1_data)
                aggregate_data.append(team2_data)
            except:
                continue

            np.savetxt("./spreads/{}.csv".format(year), aggregate_data, delimiter=",")
