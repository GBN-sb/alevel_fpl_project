# imports
from cProfile import label
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_daq as daq
import plotly.express as px
import pandas as pd
import requests

# frequently called functions________________________________________________________________________


def quicksort(arr, l, h):
    def partition(arr, l, h):
        i = (l-1)
        pivot = arr[h]

        for j in range(l, h):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i+1], arr[h] = arr[h], arr[i+1]
        return(i+1)

    if len(arr) == 1:
        return arr
    if l < h:
        partition_index = partition(arr, l, h)
        quicksort(arr, l, partition_index-1)
        quicksort(arr, partition_index+1, h)
    return(arr)


def binarySearch(arr, l, h, x):
    if h >= l:
        mid = (h + l) // 2

        if arr[mid] == x:
            # present in array
            return mid
        elif arr[mid] > x:
            return binarySearch(arr, l, mid-1, x)
        else:
            return binarySearch(arr, mid+1, h, x)
    else:
        # not present in array
        return False


def linearSearch(arr, x):
    for i in range(len(arr)):
        if arr[i] == x:
            return(i)
    return(False)

# __________________________________________________________________________________________


def getPlayerData():

    def addPos(playersDF, element_typesDF):
        # add position
        pos = playersDF.element_type.map(
            element_typesDF.set_index('id').singular_name)
        return(pos)

    def addTeams(playersDF, teamsDF):
        # add teams
        team = playersDF.team.map(
            teamsDF.set_index('id').name)
        return(team)

    URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    r = requests.get(URL)
    json = r.json()

    # retrieve the keys
    elementsDF = pd.DataFrame(json['elements'])
    teamsDF = pd.DataFrame(json['teams'])
    element_typesDF = pd.DataFrame(json['element_types'])

    # extract the relevant data
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
                            'ict_index_rank']]
    playersDF['position'] = addPos(playersDF, element_typesDF)
    playersDF['team'] = addTeams(playersDF, teamsDF)
    number_of_players = []
    for i in range(len(playersDF)):
        number_of_players.append(i)
    playersDF.insert(39, 'Index', number_of_players)
    return playersDF


class players:
    def __init__(self, playerData):
        # attributes
        self.index = playerData[39]
        self.name = playerData[0] + " " + playerData[1]
        self.team = playerData[2]
        self.minutes = playerData[3]
        self.goals = playerData[4]
        self.assists = playerData[5]
        self.clean_sheets = playerData[6]
        self.goals_conceded = playerData[7]
        self.own_goals = playerData[8]
        self.penalties_saved = playerData[9]
        self.penalties_missed = playerData[10]
        self.yellow_cards = playerData[11]
        self.red_cards = playerData[12]
        self.saves = playerData[13]
        self.form = playerData[15]
        self.dreamteam_count = playerData[16]
        self.ep_next = playerData[17]
        self.ep_this = playerData[18]
        self.in_dreamteam = playerData[19]
        self.price = playerData[20]
        self.points_per_game = playerData[21]
        self.fitness = playerData[22]
        self.total_points = playerData[23]
        self.transfers_in = playerData[24]
        self.transfers_out = playerData[25]
        self.value_form = playerData[26]
        self.value_season = playerData[27]
        self.bonus = playerData[28]
        self.bps = playerData[29]
        self.influence = playerData[30]
        self.creativity = playerData[31]
        self.threat = playerData[32]
        self.ict_index = playerData[33]
        self.influence_rank = playerData[34]
        self.creativity_rank = playerData[35]
        self.threat_rank = playerData[36]
        self.ict_index_rank = playerData[37]
        self.position = playerData[38]
        self.pick = playerData[40]
        self.rank_pick = playerData[41]

    # actions
    def getName(self):
        return(self.name)

    def getPosition(self):
        return(self.position)

    def getTeam(self):
        return(self.team)

    def getMinutes(self):
        return(self.minutes)

    def getGoals(self):
        return(self.goals)

    def getAssists(self):
        return(self.assists)

    def getCleanSheets(self):
        return(self.clean_sheets)

    def getGoalsConceded(self):
        return(self.goals_conceded)

    def getOwnGoals(self):
        return(self.own_goals)

    def getPenaltiesSaved(self):
        return(self.penalties_saved)

    def getPenaltiesMissed(self):
        return(self.penalties_missed)

    def getYellowCards(self):
        return(self.yellow_cards)

    def getRedCards(self):
        return(self.red_cards)

    def getSaves(self):
        return(self.saves)

    def getForm(self):
        return(self.form)

    def getDreamTeamCount(self):
        return(self.dreamteam_count)

    def getNextEp(self):
        return(self.ep_next)

    def getThisEp(self):
        return(self.ep_this)

    def getIsInDreamTeam(self):
        return(self.in_dreamteam)

    def getPrice(self):
        return(self.price)

    def getPointsPerGame(self):
        return(self.points_per_game)

    def getFitness(self):
        return(self.fitness)

    def getTotalPoints(self):
        return(self.total_points)

    def getTransfersIn(self):
        return(self.transfers_in)

    def getTransfersOut(self):
        return(self.transfers_out)

    def getFormValue(self):
        return(self.value_form)

    def getSeasonValue(self):
        return(self.value_season)

    def getBonus(self):
        return(self.bonus)

    def getBPS(self):
        return(self.bps)

    def getInfluence(self):
        return(self.influence)

    def getInfluenceRank(self):
        return(self.influence_rank)

    def getCreativity(self):
        return(self.creativity)

    def getCreativityRank(self):
        return(self.creativity_rank)

    def getThreat(self):
        return(self.threat)

    def getThreatRank(self):
        return(self.threat_rank)

    def getICT(self):
        return(self.ict_index)

    def getICTRank(self):
        return(self.ict_index_rank)

    def getPick(self):
        return(self.pick)

    def getRankPick(self):
        return(self.rank_pick)


def getTeamData():
    URL = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    r = requests.get(URL)
    json = r.json()
    teamsDF = pd.DataFrame(json['teams'])
    teamsDFSliced = teamsDF[['id', 'name', 'strength', 'position',
                             'strength_overall_home', 'strength_overall_away']]
    return(teamsDFSliced)


def createClassPlayersDF(df):
    # puts every player and their data into an array
    playersArr = [""] * len(df)
    tempArr = []
    for i in range(len(df.index)):
        del tempArr[:]
        for j in range(42):
            element = df.iloc[i, j]
            tempArr.append(element)
        playersArr[i] = players(tempArr)
    return(playersArr)


def assignPlayerPick(teamsDF, fixturesDF, playersDF):
    # ______________________________________________________________Functions_____________________________________________________________________________

    def match_difficulty(fixtures, difficulty, teams, playersDF):
        def getCleanSheets(playersDF):
            clean_sheets = []
            temp_cleansheets = 0

            def getGK(df):
                gk_data = df[df['position'] ==
                             'Goalkeeper'].copy().reset_index()
                return gk_data
            gkDF = getGK(playersDF)
            gkDF.sort_values(by=['team'])
            team = gkDF['team']
            team_cleansheets = gkDF['clean_sheets']
            for i in range(len(gkDF)):
                if i != 0:
                    if team[i] != team[i-1]:
                        clean_sheets.append(temp_cleansheets)
                        temp_cleansheets = 0
                temp_cleansheets += team_cleansheets[i]
            clean_sheets.append(temp_cleansheets)
            return clean_sheets

        def getGoals(playersDF):
            goals_scored = []
            temp_goals = 0
            playersDF.sort_values(by=['team'])
            team = playersDF['team']
            goals = playersDF['goals_scored']

            for i in range(len(playersDF)):
                if i != 0:
                    if team[i] != team[i-1]:
                        goals_scored.append(temp_goals)
                        temp_goals = 0
                temp_goals += goals[i]
            goals_scored.append(temp_goals)
            return goals_scored

        clean_sheets = getCleanSheets(playersDF)
        goals = getGoals(playersDF)
        zipped = list(zip(teams, goals, clean_sheets, fixtures,
                      difficulty))
        fixture_difficulty_df = pd.DataFrame(
            zipped, columns=['Team', 'Goals_scored', 'Clean_sheets', 'Next_fixtures', 'Difficulty'])
        return fixture_difficulty_df

    def getDifficultyRating(df, next_fixtures):
        def removeindex(df):
            temp = list(df)
            noIndex = temp[0]
            return(noIndex)

        home_strength = teamsDF['strength_overall_home']
        away_strength = teamsDF['strength_overall_away']
        df.insert(5, 'Home_Strength', home_strength)
        df.insert(6, 'Away_Strength', away_strength)
        attackerDifficulty = []
        defenderDifficulty = []
        currentGW = fixturesDF['event']
        currentGW = currentGW[0]
        for i in range(len(next_fixtures)):
            # number of fixtures could be greater than 3 if theres a double game week
            team_fixtures = next_fixtures[i]
            attacker_difficulty = 0
            defender_difficulty = 0
            for j in range(len(team_fixtures)):
                if team_fixtures[j] != "Blank GW":
                    next_fixture = team_fixtures[j]
                    next_fixture_df = df.loc[df['Team'] == next_fixture]
                    opponant_goals = removeindex(
                        next_fixture_df['Goals_scored'])
                    opponant_cleen_sheets = removeindex(
                        next_fixture_df['Clean_sheets'])
                    strength_home = home_strength[i]
                    strength_away = away_strength[i]
                    opponant_home_strength = removeindex(
                        next_fixture_df['Home_Strength'])
                    opponant_away_strength = removeindex(
                        next_fixture_df['Away_Strength'])
                    difficulty = df['Difficulty']
                    if difficulty[j] == "H":
                        strength_difference = int((
                            strength_home-opponant_away_strength))
                    else:
                        strength_difference = int((
                            strength_away-opponant_home_strength))
                        strength_difference = int(float(strength_difference))
                    defender_difficulty += (strength_difference+1 *
                                            (1/(opponant_goals / currentGW)))
                    attacker_difficulty += ((strength_difference+1) *
                                            (opponant_cleen_sheets / currentGW))
                else:
                    attacker_difficulty += -250
                    defender_difficulty += -250
            defender_difficulty = int(defender_difficulty)
            attacker_difficulty = int(attacker_difficulty)
            attackerDifficulty.append(attacker_difficulty)
            defenderDifficulty.append(defender_difficulty)
        df.insert(7, 'Attacker_Difficulty', attackerDifficulty)
        df.insert(8, 'Defender_Difficulty', defenderDifficulty)
        positions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                     11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        df = df.sort_values(by=['Attacker_Difficulty'])
        df.insert(8, 'Attack_Difficulty_Rank', positions)
        df = df.sort_values(by=['Defender_Difficulty'])
        df.insert(10, 'Defence_Difficulty_Rank', positions)
        df = df.sort_values(by=['Team'])
        difficultyDF = df[[
            'Team', 'Attacker_Difficulty', 'Defender_Difficulty', 'Attack_Difficulty_Rank', 'Defence_Difficulty_Rank']]
        return(difficultyDF)

    def getDefence(defences, team, teamsDF):
        teams = teamsDF['name']
        for i in range(len(teams)):
            if team == teams[i]:
                defence = defences[i]
                return defence

    def getAttack(attacks, team, teamsDF):
        teams = teamsDF['name']
        for i in range(len(teams)):
            if team == teams[i]:
                attack = attacks[i]
                return attack

    def assignGK(defences, df, teamsDF):
        gkDF = df['Index'].reset_index()
        gkIndex = []
        for i in range(len(df)):
            gkIndex.append(i)
        gkDF.insert(2, 'gk_index', gkIndex)
        results = []
        for i in range(len(gkDF)):
            team = df.iloc[gkIndex[i]]['team']
            form = int(float(df.iloc[gkIndex[i]]['form']))
            fitness = df.iloc[gkIndex[i]]['status']
            minutes = df.iloc[gkIndex[i]]['minutes']
            total_points = df.iloc[gkIndex[i]]['total_points']
            defence = getDefence(defences, team, teamsDF)
            defence = int(defence)
            # make sure player is available
            if fitness != "a" or minutes == 0:
                result = -10000
            else:
                if form > 0.5:
                    result = defence * (total_points/21)
                else:
                    result = -10000
            results.append(result)
        df.insert(40, 'pick', results)

        pick_ranks = []
        df = df.sort_values(by=['pick'], ascending=False)
        for i in range(len(df)):
            pick_ranks.append(i+1)
        df.insert(41, 'pick_rank', pick_ranks)
        return(df)

    def assignDef(defences, df, teamsDF):
        defDF = df['Index'].reset_index()
        defIndex = []
        for i in range(len(df)):
            defIndex.append(i)
        results = []
        for i in range(len(defDF)):
            threat = int(float(df.iloc[defIndex[i]]['threat']))
            team = df.iloc[defIndex[i]]['team']
            form = int(float(df.iloc[defIndex[i]]['form']))
            fitness = df.iloc[defIndex[i]]['status']
            defence = getDefence(defences, team, teamsDF)
            defence = int(defence)
            minutes = df.iloc[defIndex[i]]['minutes']
        # make sure player is available
            if fitness != "a" or minutes == 0:
                result = -500
            else:
                if form > 0.5:
                    result = defence + threat * form
                else:
                    result = 0.5
            results.append(result)
        df.insert(40, 'pick', results)

        pick_ranks = []
        df = df.sort_values(by=['pick'], ascending=False)
        for i in range(len(df)):
            pick_ranks.append(i+1)
        df.insert(41, 'pick_rank', pick_ranks)
        return(df)

    def assignMid(attacks, df, teamsDF):
        midDF = df['Index'].reset_index()
        midIndex = []
        for i in range(len(df)):
            midIndex.append(i)
        results = []
        for i in range(len(midDF)):
            threat = int(float(df.iloc[midIndex[i]]['threat']))
            creativity = int(float(df.iloc[midIndex[i]]['creativity']))
            team = df.iloc[midIndex[i]]['team']
            form = int(float(df.iloc[midIndex[i]]['form']))
            fitness = df.iloc[midIndex[i]]['status']
            attack = getAttack(attacks, team, teamsDF)
            attack = int(attack)
            minutes = df.iloc[midIndex[i]]['minutes']
        # make sure player is available
            if fitness != "a" or minutes == 0:
                result = 0
            else:
                if form > 0.5:
                    result = int(attack + threat * form)
                else:
                    result = -500
            results.append(result)
        df.insert(40, 'pick', results)

        pick_ranks = []
        df = df.sort_values(by=['pick'], ascending=False)
        for i in range(len(df)):
            pick_ranks.append(i+1)
        df.insert(41, 'pick_rank', pick_ranks)
        return(df)

    def assignFwd(attacks, df, teamsDF, fixturesDF):
        fwdDF = df['Index'].reset_index()
        fwdIndex = []
        for i in range(len(df)):
            fwdIndex.append(i)
        results = []
        for i in range(len(fwdDF)):
            threat = int(float(df.iloc[fwdIndex[i]]['threat']))
            team = df.iloc[fwdIndex[i]]['team']
            form = int(float(df.iloc[fwdIndex[i]]['form']))
            goals = int(df.iloc[fwdIndex[i]]['goals_scored'])
            fitness = df.iloc[fwdIndex[i]]['status']
            attack = getDefence(attacks, team, teamsDF)
            attack = int(attack)
            currentGW = fixturesDF['event']
            currentGW = int(currentGW[0])
            minutes = df.iloc[fwdIndex[i]]['minutes']
        # make sure player is available
            if fitness != "a" or minutes == 0:
                result = 0
            else:
                if form > 0.5:
                    result = int(attack + threat * (goals/90) * form)
                else:
                    result = -500
            results.append(result)
        df.insert(40, 'pick', results)

        pick_ranks = []
        df = df.sort_values(by=['pick'], ascending=False)
        for i in range(len(df)):
            pick_ranks.append(i+1)
        df.insert(41, 'pick_rank', pick_ranks)
        return(df)

    def nextFixtures(teams, fixturesDF):
        # ______________________________________________________________functions_____________________________________________________________________________
        def getMatches(df):
            current_gw = df.iloc[0]['event']
            gw = current_gw
            gw1 = []
            gw2 = []
            gw3 = []
            for i in range(len(df)):
                if gw != current_gw + 3:
                    if df.iloc[i]['event'] == current_gw:
                        gw1.append(df.iloc[i]['team_h'])
                        gw1.append(df.iloc[i]['team_a'])
                    elif df.iloc[i]['event'] == current_gw + 1:
                        gw2.append(df.iloc[i]['team_h'])
                        gw2.append(df.iloc[i]['team_a'])
                    elif df.iloc[i]['event'] == current_gw + 2:
                        gw3.append(df.iloc[i]['team_h'])
                    gw = df.iloc[i]['event']
            return gw1, gw2, gw3

        def addToArray(matches, match_venue, arr):
            for j in range(len(arr)):
                if arr[j] == team:
                    if (j+2) % 2 == 0:
                        matches.append(arr[j+1])
                        match_venue.append('H')
                    else:
                        matches.append(arr[j-1])
                        match_venue.append('A')
            return matches, match_venue

        # ______________________________________________________________main code_____________________________________________________________________________
        first_GW, second_GW, third_GW = getMatches(fixturesDF)
        next_fixtures = []
        next_fixtures_difficulty = []

        for i in range(len(teams)):
            team = teams[i]
            matches = []
            match_venue = []
            matches, match_venue = addToArray(
                matches, match_venue, first_GW)

            if len(matches) < 1:
                matches.append("Blank GW")
                match_venue.append("B")

            matches_len = len(matches)

            matches, match_venue = addToArray(
                matches, match_venue, second_GW)

            if len(matches) == matches_len:
                matches.append("Blank GW")
                match_venue.append("B")

            matches_len = len(matches)

            matches, match_venue = addToArray(
                matches, match_venue, third_GW)

            if len(matches) == matches_len:
                matches.append("Blank GW")
                match_venue.append("B")

            next_fixtures.append(matches)
            next_fixtures_difficulty.append(match_venue)
        return next_fixtures, next_fixtures_difficulty
    # ______________________________________________________________main code_____________________________________________________________________________
    teams = ['Arsenal', 'Aston Villa', 'Brentford', 'Brighton', 'Burnley', 'Chelsea', 'Crystal Palace', 'Everton', 'Leeds', 'Leicester',
             'Liverpool', 'Man City', 'Man Utd', 'Newcastle', 'Norwich', 'Southampton', 'Spurs', 'Watford', 'West Ham', 'Wolves']

    next_fixtures, next_fixtures_difficulty = nextFixtures(teams, fixturesDF)

    fixture_difficulty_df = match_difficulty(next_fixtures, next_fixtures_difficulty,
                                             teams, playersDF)
    difficultyDF = getDifficultyRating(fixture_difficulty_df,
                                       next_fixtures)
    attacks = difficultyDF['Attacker_Difficulty']
    defences = difficultyDF['Defender_Difficulty']
    goalkeeperDF = playersDF[playersDF['position'] == 'Goalkeeper'].copy()
    defenderDF = playersDF[playersDF['position'] == 'Defender'].copy()
    midfielderDF = playersDF[playersDF['position'] == 'Midfielder'].copy()
    forwardDF = playersDF[playersDF['position'] == 'Forward'].copy()
    gkDF = assignGK(defences, goalkeeperDF, teamsDF)
    defDF = assignDef(defences, defenderDF, teamsDF)
    midDF = assignMid(attacks, midfielderDF, teamsDF)
    fwdDF = assignFwd(attacks, forwardDF, teamsDF, fixturesDF)
    dataFrames = [gkDF, defDF, midDF, fwdDF]
    # merge all frames
    playersDFwithPick = pd.concat(dataFrames)
    return(gkDF, defDF, midDF, fwdDF, playersDFwithPick)


def fixtures(teamsDF):
    URL = 'https://fantasy.premierleague.com/api/fixtures?future=1'
    r = requests.get(URL)
    json = r.json()
    fixture = pd.DataFrame(json)
    fixtureDF = fixture[['event', 'team_a', 'team_h']]
    fixtureDF['team_a'] = fixtureDF.team_a.map(
        teamsDF.set_index('id').name)
    fixtureDF['team_h'] = fixtureDF.team_h.map(
        teamsDF.set_index('id').name)
    fixtureDF = fixtureDF.head(30)
    return fixtureDF


def getStartingXI(playersDF, OOP):
    # ______________________________________________________________Functions_____________________________________________________________________________
    def getFullNames(nameDF):
        names_Arr = []
        for i in range(len(nameDF)):
            name = str(nameDF.iloc[i]['first_name']) + ' ' + \
                str(nameDF.iloc[i]['second_name'])
            names_Arr.append(name)
        return(names_Arr)

    def getDataFrame(names_Arr, names_positions, pick_rank):
        dict = {'full_name': names_Arr,
                'position': names_positions,
                'pick_rank': pick_rank}
        df = pd.DataFrame(dict)
        original_index = []
        for i in range(len(df)):
            original_index.append(i)
        df['original_index'] = original_index
        return(df)

    def checkIfValid(x, df):
        df = df['full_name']
        names = []
        for i in range(len(df)):
            name = str(df.iloc[i])
            names.append(name)
        valid = linearSearch(names, x)
        return(valid)

    def getGK(df, FORMATION, TITLES):
        numberOfPlayers = FORMATION[0]
        goalkeepers = []
        for i in range(numberOfPlayers):
            valid = False
            while True:
                name = input("Enter %s goalkeeper: " % TITLES[i])
                if name in goalkeepers:
                    valid = False
                else:
                    if checkIfValid(name, df) != False:
                        goalkeepers.append(name)
                        valid = True
                if valid == True:
                    break
        return(goalkeepers)

    def getDef(df, FORMATION, TITLES):
        numberOfPlayers = FORMATION[1]
        defenders = []
        for i in range(numberOfPlayers):
            valid = False
            while True:
                name = input('Enter %s defender: ' % TITLES[i])
                if name in defenders:
                    valid = False
                else:
                    if checkIfValid(name, df) != False:
                        defenders.append(name)
                        valid = True
                if valid == True:
                    break
        return(defenders)

    def getMid(df, FORMATION, TITLES):
        numberOfPlayers = FORMATION[2]
        midfielders = []
        for i in range(numberOfPlayers):
            valid = False
            while True:
                name = input('Enter %s midfielder: ' % TITLES[i])
                if name in midfielders:
                    valid = False
                else:
                    if checkIfValid(name, df) != False:
                        midfielders.append(name)
                        valid = True
                if valid == True:
                    break
        return(midfielders)

    def getFWd(df, FORMATION, TITLES):
        numberOfPlayers = FORMATION[3]
        forwards = []
        for i in range(numberOfPlayers):
            valid = False
            while True:
                name = input('Enter %s forward: ' % TITLES[i])
                if name in forwards:
                    valid = False
                else:
                    if checkIfValid(name, df) != False:
                        forwards.append(name)
                        valid = True
                if valid == True:
                    break
        return(forwards)

    def getStats(startingXI, OOP, df):
        indexes = []
        for i in range(len(startingXI)):
            players_in_position = startingXI[i]
            for j in range(len(players_in_position)):
                indexes.append(df.index[df['full_name'] ==
                                        players_in_position[j]].tolist())
        id = []
        name = []
        pick = []
        for i in range(len(indexes)):
            j = indexes[i][0]
            id.append(j)
            name.append(players.getName(OOP[j]))
            pick.append(players.getRankPick(OOP[j]))
        data = {"ID": id, "Name": name, "Pick": pick}
        startingXIdf = pd.DataFrame(data)
        transfer_out = startingXIdf.sort_values(by='Pick', ascending=False)
        return(transfer_out)

    # ______________________________________________________________Main Code_____________________________________________________________________________
    playersDF = playersDF[['first_name',
                           'second_name', 'position', 'pick_rank']]
    names_Arr = getFullNames(playersDF)
    name_position = list(playersDF['position'])
    pick_rank = list(playersDF['pick_rank'])
    df = getDataFrame(names_Arr, name_position, pick_rank)
    gkDF = df[df['position'] == 'Goalkeeper'].copy()
    defDF = df[df['position'] == 'Defender'].copy()
    midDF = df[df['position'] == 'Midfielder'].copy()
    fwdDF = df[df['position'] == 'Forward'].copy()
    startingXI = []
    FORMATION = [2, 5, 5, 3]
    TITLES = ['first', 'second', 'third', 'fourth', 'fifth']
    # goalkeepers = getGK(gkDF, FORMATION, TITLES)
    # defenders = getDef(defDF, FORMATION, TITLES)
    # midfielders = getMid(midDF, FORMATION, TITLES)
    # forwards = getFWd(fwdDF, FORMATION, TITLES)
    # startingXI = np.concatenate((goalkeepers, defenders, midfielders, forwards), axis=0)
    startingXI = [['Robert Sánchez', 'Aaron Ramsdale'], ['Trent Alexander-Arnold', 'João Pedro Cavaco Cancelo', 'Marc Guéhi', 'Reece James', 'Tino Livramento'], [
        'Mohamed Salah', 'Diogo Jota', 'Bernardo Mota Veiga de Carvalho e Silva', 'Lucas Rodrigues Moura da Silva', 'Conor Gallagher'], ['Neal Maupay', 'Emmanuel Dennis', 'Christian Benteke']]
    return(getStats(startingXI, OOP, df))


def suggestTransfer(df, teamDF, OOP):
    def get_players(teamDF):
        player_list = []
        for i in range(len(teamDF)):
            indexDF = teamDF['ID']
            player = indexDF[i]
            player_list.append(player)
        return(player_list)

    def getTransfers(player, players_in_team, df, OOP):
        sell_price = players.getPrice(OOP[player])
        sell_pos = players.getPosition(OOP[player])
        sell_pick = players.getPick(OOP[player])
        sell_name = players.getName(OOP[player])
        df = df[df['position'] == sell_pos].sort_values(
            by='pick', ascending=False).reset_index()
        player_in = df['index']
        for i in range(len(df)):
            x = player_in[i]
            not_valid = linearSearch(players_in_team, x)
            price = players.getPrice(OOP[x])
            pick = players.getRankPick(OOP[x])
            name = players.getName(OOP[x])
            if not_valid == False and price <= sell_price and pick > sell_pick:
                transfer = (sell_name + " -> " + name)
                return(transfer)
        return("None")

    # get 5 worse players
    teamDF = teamDF.sort_values(by='Pick', ascending=False)
    player_out = teamDF.head(5).reset_index()
    # get a list of existing players indexes
    players_in_team = get_players(teamDF)
    # loop through each player finding a transfer
    transfers = []
    for i in range(len(player_out)):
        player = player_out.loc[i]['ID']
        transfers.append(getTransfers(player, players_in_team, df, OOP))
    return(transfers)


def display(OOP, df):
    # GUI
    app = dash.Dash(__name__)
    print(df)
    playersDF = df['Index']
    values = list(playersDF)
    labels = []
    for i in range(len(values)):
        player = players.getName(OOP[values[i]])
        labels.append(player)

    options = [{'label': labels[i], 'value':values[i]}
               for i in range(len(labels))]

    app.layout = html.Div([
        dcc.Dropdown(
            id='player-dropdown',
            options=options,
            style={'margin-top': '50px', 'margin-left': '50px'}
        ),
        html.Div(id='player-id-output')
    ])

    @app.callback(
        Output('player-id-output', 'children'),
        Input('player-dropdown', 'value')
    )
    def update_output(value):
        return None

    app.run_server(debug=True)


def main():
    playerDF = getPlayerData()
    teamsDF = getTeamData()
    fixtureDF = fixtures(teamsDF)
    gkDF, defDF, midDF, fwdDF, playersDFwithPick = assignPlayerPick(
        teamsDF, fixtureDF, playerDF)

    # testing ___________________________________________________________________________________________
    tempDF = playersDFwithPick[['first_name', 'second_name',
                                'team', 'clean_sheets', 'position', 'pick', 'pick_rank']]
    tempDF = tempDF.sort_values(by=['pick_rank'])
    playersDFwithPick = playersDFwithPick.sort_values(by=['Index'])
    OOP = createClassPlayersDF(playersDFwithPick)
    startingXIdf = getStartingXI(playersDFwithPick, OOP)

    suggest_transfers = suggestTransfer(playersDFwithPick, startingXIdf, OOP)

    print(suggest_transfers)

    startingXI = [['Ederson Santana de Moraes', 'José Malheiro de Sá'], ['Emerson Aparecido Leite de Souza Junior', 'Ben Mee', 'Dan Burn', 'Ben White', 'Rúben Santos Gato Alves Dias'], [
        'Juan Mata', 'João Filipe Iria Santos Moutinho', 'Bernardo Mota Veiga de Carvalho e Silva', 'Joe White', 'Frederico Rodrigues de Paula Santos'], ['Cristiano Ronaldo dos Santos Aveiro', 'Danny Ings', 'Pierre-Emerick Aubameyang']]
    freeTransfers = 1
    display(OOP, playersDFwithPick)


if __name__ == "__main__":
    main()
