# imports
import pandas as pd
import requests

# _______________________get player data___________________________


def addPos(playersDF, element_typesDF):
    # asign each player their position
    pos = playersDF.element_type.map(
        element_typesDF.set_index('id').singular_name)
    return(pos)


def addTeams(playersDF, teamsDF):
    # assign each player their team
    team = playersDF.team.map(
        teamsDF.set_index('id').name)
    return(team)


def getPlayerDataFrame():
    # api URL
    URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    # the return of the request containing the player data from the api
    r = requests.get(URL)
    # convert to a readable format
    json = r.json()
    # retrieve the keys
    elementsDF = pd.DataFrame(json['elements'])
    teamsDF = pd.DataFrame(json['teams'])
    element_typesDF = pd.DataFrame(json['element_types'])

    # extract the relevant data columns
    playersDF = elementsDF[['first_name', 'second_name', 'team', 'minutes', 'goals_scored',
                            'assists', 'clean_sheets', 'goals_conceded', 'own_goals',
                            'penalties_saved', 'penalties_missed', 'yellow_cards', 'red_cards',
                            'saves', 'element_type', 'form', 'dreamteam_count', 'ep_next',
                            'ep_this', 'in_dreamteam',
                            'now_cost', 'points_per_game',
                            'status', 'total_points', 'transfers_in',
                            'transfers_out',
                            'value_form', 'value_season', 'bonus', 'bps', 'influence', 'creativity', 'threat',
                            'ict_index', 'influence_rank', 'creativity_rank',
                            'threat_rank',
                            'ict_index_rank'
                            ]]
    # map each players team and position
    playersDF['position'] = addPos(playersDF, element_typesDF)
    playersDF['team'] = addTeams(playersDF, teamsDF)
    # create a column containg players orignal index value
    playersDF['original_index'] = range(0, len(playersDF))
    # merge first and last names to create full names
    playersDF['name'] = playersDF['first_name'] + \
        ' ' + playersDF['second_name']
    # remove accents
    playersDF['name'] = playersDF['name'].str.normalize('NFKD').str.encode(
        'ascii', errors='ignore').str.decode('utf-8')
    return(playersDF)


# ____________________teamDF______________________________
def getCleanSheets(df):
    total_clean_sheets = []
    df = df[df['position'] == 'Goalkeeper']
    df = df.sort_values(by=['team'])
    prev_team = df.iloc[0]['team']
    temp = 0
    for team, clean_sheets in zip(df['team'], df['clean_sheets']):
        if team != prev_team:
            total_clean_sheets.append(temp)
            temp = 0
        temp += clean_sheets
        prev_team = team
    total_clean_sheets.append(temp)
    return(total_clean_sheets)


def getGoals(df):
    total_goals = []
    df = df.sort_values(by=['team'])
    prev_team = df.iloc[0]['team']
    temp = 0
    for team, goals in zip(df['team'], df['goals_scored']):
        if team != prev_team:
            total_goals.append(temp)
            temp = 0
        temp += goals
        prev_team = team
    total_goals.append(temp)
    return(total_goals)


def getTeamDataFrame():
    # API url
    URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    # the return of the request containing the player data from the api
    r = requests.get(URL)
    # converts the responce to a readable format
    json = r.json()
    # create database from the data under the 'teams' key
    teamsDF = pd.DataFrame(json['teams'])
    # extract the relevant data headings
    teamsDFSliced = teamsDF[['id', 'name',
                             'strength_overall_home', 'strength_overall_away']]
    # add clean sheets and goals
    teamsDFSliced['clean_sheets'] = getCleanSheets(getPlayerDataFrame())
    teamsDFSliced['goals'] = getGoals(getPlayerDataFrame())
    return(teamsDFSliced)


# _____________________fixtureDF___________________________
def getFixtureDataFrame():
    teamDF = getTeamDataFrame()
    # API url
    URL = 'https://fantasy.premierleague.com/api/fixtures?future=1'
    # get player data from the api
    r = requests.get(URL)
    # convert the return data to a readable format
    json = r.json()
    # create a dataframe from the json format
    fixture = pd.DataFrame(json)
    # extract the relevant data columns
    fixtureDF = fixture[['event', 'team_a', 'team_h']]
    # map the away teams
    fixtureDF['team_a'] = fixtureDF.team_a.map(
        teamDF.set_index('id').name)
    # map the home teams
    fixtureDF['team_h'] = fixtureDF.team_h.map(
        teamDF.set_index('id').name)
    return(fixtureDF)
