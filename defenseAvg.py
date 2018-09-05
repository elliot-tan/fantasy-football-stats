import pandas as pd
import numpy as np

df = pd.read_csv('spreadspoke_scores.csv')

#we need to grab the date, season, teams, and scores
modernDF = df[(df.schedule_season==2017)][['schedule_season','schedule_date','team_home','team_away','score_home','score_away']]

#Create teams dict
teams = {}
#Fill teams dict, add in nested for conceded points home, away, and played
for index, row in modernDF.iterrows():
    teams[row.team_home] = {'conceded_home': 0, 'conceded_away': 0, 'games': 0}

#populate dict; if the team is home, add in score of away team and vice versa
for index, row in modernDF.iterrows():
    teams[row.team_home]['conceded_away'] += row.score_away
    teams[row.team_home]['games'] += 1
    teams[row.team_away]['conceded_home'] += row.score_home
    teams[row.team_away]['games'] += 1

#Place results into a data frame 
df3 = pd.DataFrame.from_dict(teams).T #flip axes
df3['avg_concede'] = (df3.conceded_away +df3.conceded_home)/df3.games
df3['away_avg'] = df3.conceded_away/(df3.games/2)
df3['home_avg']= df3.conceded_home/(df3.games/2)


print("Lowest away avg is " + str(df3.away_avg.min()),df3.index[df3.away_avg == df3.away_avg.min()].tolist())
print("Lowest home avg is " + str(df3.home_avg.min()),df3.index[df3.home_avg == df3.home_avg.min()].tolist())
print("Lowest avg is " + str(df3.avg_concede.min()),df3.index[df3.avg_concede == df3.avg_concede.min()].tolist())
