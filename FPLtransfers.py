# imports
import FPLCompleteData as data

# test data
startingXI = ['Robert Sánchez', 'Aaron Ramsdale', 'Trent Alexander-Arnold', 'João Pedro Cavaco Cancelo', 'Marc Guéhi', 'Reece James', 'Tino Livramento',
              'Mohamed Salah', 'Diogo Jota', 'Bernardo Mota Veiga de Carvalho e Silva', 'Lucas Rodrigues Moura da Silva', 'Conor Gallagher', 'Neal Maupay', 'Emmanuel Dennis', 'Christian Benteke']


def getSingleTransfer(squad_df, pos_df, invalid_teams, name, price, pick, team):
    for buy_name, buy_price, buy_pick, buy_team in zip(pos_df['name'], pos_df['now_cost'], pos_df['pick_rank'], pos_df['team']):
        # check if buy player is not already in the team
        valid = not(buy_name in squad_df['name'].unique())
        # check if the buy player is better than the sell player and is afforable
        if valid == True and buy_price <= price and buy_pick < pick and (not(buy_team in invalid_teams) or buy_team == team):
            transfer = (name + " -> " + buy_name)
            return(transfer)
    return('None')


def getMultipleTransfers(squad_df, df, invalid_teams, p1_name, p1_position, p1_rank, p1_team, p2_name, p2_position, p2_rank, p2_team, budget):
    # check if both players positions are the same
    if p1_position == p2_position:
        pos_df = df[df['position'] == p1_position].sort_values(
            by='pick_rank', ascending=True)
        for buy_p1_name, buy_p1_price, buy_p1_rank, buy_p1_team in zip(pos_df['name'], pos_df['now_cost'], pos_df['pick_rank'], pos_df['team']):
            # check if p1 is not already in the team
            if not(buy_p1_name in squad_df['name'].unique()) and (not(buy_p1_team in invalid_teams) or (buy_p1_team == p1_team or p2_team)):
                pos_df = pos_df[pos_df.name != buy_p1_name]
                for i in range(2):
                    buy_p2_name = pos_df.iloc[i]['name']
                    # check if ps is not already in the team
                    buy_p2_team = pos_df.iloc[i]['team']
                    if not(buy_p1_name in squad_df['name'].unique()) and (not(buy_p2_team in invalid_teams) or (buy_p2_team == (p1_team or p2_team) and not(buy_p1_team))):
                        buy_p2_price = pos_df.iloc[i]['now_cost']
                        buy_p2_rank = pos_df.iloc[i]['pick_rank']
                        buy_cost = int(buy_p1_price) + int(buy_p2_price)
                        buy_pick = int(buy_p1_rank) + int(buy_p2_rank)
                        total_pick = int(p1_rank) + int(p2_rank)
                        if buy_cost <= budget and buy_pick < total_pick:
                            transfer = ('(%s) & (%s) -> (%s) & (%s)' %
                                        (p1_name, p2_name, buy_p1_name, buy_p2_name))
                            return(transfer)
        return('None')

    else:
        p1_pos_df = df[df['position'] == p1_position].sort_values(
            by='pick_rank', ascending=True)
        p2_pos_df = df[df['position'] == p2_position].sort_values(
            by='pick_rank', ascending=True)


def suggestTransfer(squad, transfers):
    df = data.getPlayerData()
    # get data for the squad
    squad_df = df.loc[df['name'].isin(squad)]
    # create transfer list to append to later
    transfers = []
    # suggest 5 players to transfer out
    players_out_df = squad_df.sort_values(
        by='pick_rank', ascending=False).head(5)
    # check if their are 3 palyers from any team already in the squad
    invalid_teams = squad_df.pivot_table(
        columns=['team'], aggfunc='size')
    invalid_teams = invalid_teams[invalid_teams == 3] == True
    invalid_teams = list(invalid_teams.index)
    # check how many transfers are available
    if transfers == 1:
        for name, position, price, pick, team in zip(players_out_df['name'], players_out_df['position'], players_out_df['now_cost'], players_out_df['pick_rank'], players_out_df['team']):
            pos_df = df[df['position'] == position].sort_values(
                by='pick_rank', ascending=True)
            transfers.append(getSingleTransfer(
                squad_df, pos_df, invalid_teams, name, price, pick, team))
    else:
        for p1_name, p1_team, p1_position, p1_price, p1_rank in zip(players_out_df['name'], players_out_df['team'], players_out_df['position'], players_out_df['now_cost'], players_out_df['pick_rank']):
            # remove player
            players_out_df = players_out_df[players_out_df.name != p1_name]
            for p2_name, p2_team, p2_position, p2_price, p2_rank in zip(players_out_df['name'], players_out_df['team'], players_out_df['position'], players_out_df['now_cost'], players_out_df['pick_rank']):
                budget = int(p1_price) + int(p2_price)
                transfers.append(getMultipleTransfers(squad_df, df, invalid_teams, p1_name,
                                 p1_position, p1_rank, p1_team, p2_name, p2_position, p2_rank, p2_team, budget))
    print(transfers)


suggestTransfer(startingXI, 2)
