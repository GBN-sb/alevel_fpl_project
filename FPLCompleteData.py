# imports
import pandas as pd
import FPLDataframes as DFs
import FPLFixtures as fixtures

# calculate and rank how well each player will perform

# Goalkeepers


def assignGK(playerDF, teamDF):
    results = []
    for team, minutes, status, form, points in zip(playerDF['team'], playerDF['minutes'], playerDF['status'], playerDF['form'], playerDF['total_points']):
        defence = int(teamDF.loc[teamDF['name'] ==
                      team, 'defender_difficulty'])
        # filter out players who don't start regularly
        if status != 'a' or minutes == 0 or int(float(form)) < 0.5:
            result = -10000
        else:
            # calculate the transfer in score
            result = (defence * int(float(form)))/1000
        results.append(result)
    # create new column for data
    playerDF['transfer_score'] = results
    # add rank
    pick_ranks = []
    playerDF = playerDF.sort_values(by=['transfer_score'], ascending=False)
    for i in range(len(playerDF)):
        pick_ranks.append(i+1)
    playerDF['pick_rank'] = pick_ranks
    return(playerDF)


# Defenders
def assignDef(playerDF, teamDF):
    results = []
    for team, threat, form, status, minutes in zip(playerDF['team'], playerDF['threat'], playerDF['form'], playerDF['status'], playerDF['minutes']):
        defence = int(teamDF.loc[teamDF['name'] ==
                                 team, 'defender_difficulty'])
       # filter out players who don't start regularly
        if status != 'a' or minutes == 0 or int(float(form)) < 0.5:
            result = -10000
        else:
            # calculate the transfer in score
            result = ((defence + int(float(threat))) * int(float(form)))/1000
        results.append(result)
    # create new column for data
    playerDF['transfer_score'] = results
    # add rank
    pick_ranks = []
    playerDF = playerDF.sort_values(by=['transfer_score'], ascending=False)
    for i in range(len(playerDF)):
        pick_ranks.append(i+1)
    playerDF['pick_rank'] = pick_ranks
    return(playerDF)


# Midfielders
def assignMid(playerDF, teamDF):
    results = []
    for team, threat, form, status, minutes in zip(playerDF['team'], playerDF['threat'], playerDF['form'], playerDF['status'], playerDF['minutes']):
        attack = int(teamDF.loc[teamDF['name'] ==
                                team, 'attacker_difficulty'])
       # filter out players who don't start regularly
        if status != 'a' or minutes == 0 or int(float(form)) < 0.5:
            result = -10000
        else:
            # calculate the transfer in score
            result = ((attack + int(float(threat))) * int(float(form)))/1000
        results.append(result)
    # create new column for data
    playerDF['transfer_score'] = results
    # add rank
    pick_ranks = []
    playerDF = playerDF.sort_values(by=['transfer_score'], ascending=False)
    for i in range(len(playerDF)):
        pick_ranks.append(i+1)
    playerDF['pick_rank'] = pick_ranks
    return(playerDF)

# Forwards


def assignFwd(playerDF, teamDF):
    results = []
    for team, threat, form, status, minutes, goals in zip(playerDF['team'], playerDF['threat'], playerDF['form'], playerDF['status'], playerDF['minutes'], playerDF['goals_scored']):
        attack = int(teamDF.loc[teamDF['name'] ==
                                team, 'attacker_difficulty'])
       # filter out players who don't start regularly
        if status != 'a' or minutes == 0 or int(float(form)) < 0.5:
            result = -10000
        else:
            # calculate the transfer in score
            result = (((attack + int(float(threat))) * (goals/90))
                      * int(float(form)))/1000
        results.append(result)
    # create new column for data
    playerDF['transfer_score'] = results
    # add rank
    pick_ranks = []
    playerDF = playerDF.sort_values(by=['transfer_score'], ascending=False)
    for i in range(len(playerDF)):
        pick_ranks.append(i+1)
    playerDF['pick_rank'] = pick_ranks
    return(playerDF)

# get position specific dataframe


def getPosition(pos, df):
    df = df[df['position'] == pos].copy()
    return(df)


# main
def getPlayerData():
    teamDF = fixtures.getFixtureDF()
    playerDF = DFs. getPlayerDataFrame()
    gkDF = getPosition('Goalkeeper', playerDF)
    defDF = getPosition('Defender', playerDF)
    midDF = getPosition('Midfielder', playerDF)
    fwDF = getPosition('Forward', playerDF)
    # get data frames with transfer in rank
    goalkeeperDF = assignGK(gkDF, teamDF)
    defenderDF = assignDef(defDF, teamDF)
    midfielderDF = assignMid(midDF, teamDF)
    forwardDF = assignFwd(fwDF, teamDF)
    # merge dataFrames together
    dataframes = [goalkeeperDF, defenderDF, midfielderDF, forwardDF]
    playerDFwithTransfer = pd.concat(dataframes).sort_index()
    return(playerDFwithTransfer)
