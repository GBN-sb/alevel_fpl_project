# imports
import FPLDataframes as dfs

# get next 3 gameweek matches


def getMatches(df, x):
    # get current gameweek number
    current_gw = df.iloc[0]['event']
    # removing any row with a higher event than the current gameweek + x
    df = df.loc[df['event'] < current_gw+x]
    return(df)

# get each teams next matches


def assignTeamFixtures(x):
    teamDF = dfs.getTeamDataFrame()  # teams
    fixtureDF = dfs.getFixtureDataFrame()  # fixtures
    # next how ever many gameweek matchs
    fixtureDF = getMatches(fixtureDF, x)
    all_team_fixtures = []
    all_fixture_stadiums = []
    # loop through all teams and assign them their next matches
    for team in teamDF['name']:
        team_fixtures = []  # contains a teams next opponants
        # contains the stadium location for each match (home/away)
        match_stadiums = []
        # contain the gw of the matches to calculate if there is a blank gameweek
        fixtures_in_gw = []
        temp_gw = fixtureDF.iloc[0]['event']
        # loop through each match and get the home and away team
        for home, away, gw in zip(fixtureDF['team_h'], fixtureDF['team_a'], fixtureDF['event']):
            # if there is no gameweek assign 'black gamewwek'
            if gw != temp_gw and not(temp_gw in fixtures_in_gw):
                team_fixtures.append('blank')
                match_stadiums.append('b')
                fixtures_in_gw.append(temp_gw)
            # if there is a match, append the opponant to the array
            if team == home:
                team_fixtures.append(away)
                match_stadiums.append('h')
                fixtures_in_gw.append(gw)
            elif team == away:
                team_fixtures.append(home)
                match_stadiums.append('a')
                fixtures_in_gw.append(gw)
            temp_gw = gw
        # check if there was a blank in the final gw
        if not(gw in fixtures_in_gw):
            team_fixtures.append('blank')
            match_stadiums.append('b')
            fixtures_in_gw.append(gw)
        all_team_fixtures.append(team_fixtures)
        all_fixture_stadiums.append(match_stadiums)
    # add data to the teamsDF
    teamDF['next_matches'] = all_team_fixtures
    teamDF['next_matches_stadiums'] = all_fixture_stadiums
    return(teamDF)

# get postion difficulty


def getFixtureDF():
    teamDF = assignTeamFixtures(3)  # team dataframe\
    fixtureDF = dfs.getFixtureDataFrame()
    matches_played = int(fixtureDF.iloc[0]['event']) - 1
    total_attacker_dif = []
    total_defender_dif = []
    # loop through each team and their data
    for team, home_strength, away_strength, matches, stadiums in zip(teamDF['name'], teamDF['strength_overall_home'], teamDF['strength_overall_away'], teamDF['next_matches'], teamDF['next_matches_stadiums']):
        attacker_dif = 0
        defender_dif = 0
        # loop through each teams fixtures
        for fixture, stadium in zip(matches, stadiums):
            opponantDF = teamDF[teamDF['name'] == fixture]  # opponant data
            # check for a blank gameweek
            if stadium != 'b':
                # get the match venue
                if stadium == 'h':
                    # calculate the strength difficulty and power the result to remove negative numbers
                    strength_difference = int(
                        home_strength - opponantDF.iloc[0]['strength_overall_away'])
                elif stadium == 'a':
                    strength_difference = int(
                        away_strength - opponantDF.iloc[0]['strength_overall_home'])
                # avoid a differende of 0
                strength_difference += 1
                op_clean_sheets = opponantDF.iloc[0]['clean_sheets']
                # calculate the difficulty for the attackers and divide by 1000 to make the numbers easier to work with
                attacker_dif += ((strength_difference) *
                                 (op_clean_sheets/matches_played))
                op_goals = opponantDF.iloc[0]['goals']
                # calculate the difficulty for the defenders
                defender_dif += ((strength_difference) *
                                 (matches_played/op_goals))
            else:  # blank gameweek penalty
                attacker_dif += -100
                defender_dif += -100
        total_attacker_dif.append(attacker_dif)
        total_defender_dif.append(defender_dif)
    # create column in the dataframe for the new lists
    teamDF['attacker_difficulty'] = total_attacker_dif
    teamDF['defender_difficulty'] = total_defender_dif
    return(teamDF)
