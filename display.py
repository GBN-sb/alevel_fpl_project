# imports
from tkinter import *

from matplotlib import backend_managers
import FPLCompleteData as fpl
import FPLtransfers as t
from tkinter import *
import plotly.express as px


def display():
    df = fpl.getPlayerData()
    # gets available labels

    def getLabels(df):
        invalid_players = []
        XI = [gk1, gk2, def1, def2, def3, def4, def5,
              mid1, mid2, mid3, mid4, mid5, fw1, fw2, fw3]
        for i in range(15):
            invalid_players.append(XI[i].cget("text"))

        if gk1.cget("text") != "GK" and gk2.cget("text") != "GK":
            df = df[df["position"].str.contains("Goalkeeper") == False]
        if def1.cget("text") != "Def" and def2.cget("text") != "Def" and def3.cget("text") != "Def" and def4.cget("text") != "Def" and def5.cget("text") != "Def":
            df = df[df["position"].str.contains("Defender") == False]
        if mid1.cget("text") != "Mid" and mid2.cget("text") != "Mid" and mid3.cget("text") != "Mid" and mid4.cget("text") != "Mid" and mid5.cget("text") != "Mid":
            df = df[df["position"].str.contains("Midfielder") == False]
        if fw1.cget("text") != "FW" and fw2.cget("text") != "FW" and fw3.cget("text") != "FW":
            df = df[df["position"].str.contains("Forward") == False]
        labels = []
        for player in df['name']:
            if player in invalid_players:
                None
            else:
                labels.append(player)
        return labels

    # update listbox

    def update(data):
        # clear list box
        player_search_list.delete(0, END)
        # add players
        for player in data:
            player_search_list.insert(END, player)

    # update label with selected item
    def fillout(event):
        search_player.delete(0, END)
        search_player.insert(0, player_search_list.get(ACTIVE))

    # check entry is in list box
    def check(event):
        labels = getLabels(df)
        typed = search_player.get()
        if typed == '':
            data = labels
        else:
            data = []
            for player in labels:
                if typed.lower() in player.lower():
                    data.append(player)
        update(data)

    # submit player choice

    def submit():
        # check valid player
        player = search_player.get()
        players_added.append(player)
        labels = getLabels(df)

        if player in labels:
            # for name, position in zip(players['name'], players['position']):
            #     if name == player:
            #         player_position = position
            #         break
            player_position = df.loc[df['name']
                                     == player, 'position'].item()
            if player_position == "Goalkeeper":
                if gk1.cget("text") == "GK":
                    gk1.config(text=player)
                else:
                    gk2.config(text=player)
            elif player_position == "Defender":
                if def1.cget("text") == "Def":
                    def1.config(text=player)
                elif def2.cget("text") == "Def":
                    def2.config(text=player)
                elif def3.cget("text") == "Def":
                    def3.config(text=player)
                elif def4.cget("text") == "Def":
                    def4.config(text=player)
                else:
                    def5.config(text=player)
            elif player_position == "Midfielder":
                if mid1.cget("text") == "Mid":
                    mid1.config(text=player)
                elif mid2.cget("text") == "Mid":
                    mid2.config(text=player)
                elif mid3.cget("text") == "Mid":
                    mid3.config(text=player)
                elif mid4.cget("text") == "Mid":
                    mid4.config(text=player)
                else:
                    mid5.config(text=player)
            else:
                if fw1.cget("text") == "FW":
                    fw1.config(text=player)
                elif fw2.cget("text") == "FW":
                    fw2.config(text=player)
                else:
                    fw3.config(text=player)
            labels = getLabels(df)
            update(labels)
            search_player.delete(0, END)

    def clearLabels():
        gk1.config(text="GK")
        gk2.config(text="GK")
        def1.config(text="Def")
        def2.config(text="Def")
        def3.config(text="Def")
        def4.config(text="Def")
        def5.config(text="Def")
        mid1.config(text="Mid")
        mid2.config(text="Mid")
        mid3.config(text="Mid")
        mid4.config(text="Mid")
        mid5.config(text="Mid")
        fw1.config(text="FW")
        fw2.config(text="FW")
        fw3.config(text="FW")
        # clear transfer suggestion box
        transfer_list_box.delete(0, END)
        # update labels
        labels = getLabels(df)
        update(labels)

    def getSquad():
        squad = []  # empty squad
        # get all default label values
        default = ['GK', 'Def', 'Mid', 'FW']
        # get players inputed by the user and add to squad list
        squad.append(gk1.cget("text"))
        squad.append(gk2.cget("text"))
        squad.append(def1.cget("text"))
        squad.append(def2.cget("text"))
        squad.append(def3.cget("text"))
        squad.append(def4.cget("text"))
        squad.append(def5.cget("text"))
        squad.append(mid1.cget("text"))
        squad.append(mid2.cget("text"))
        squad.append(mid3.cget("text"))
        squad.append(mid4.cget("text"))
        squad.append(mid5.cget("text"))
        squad.append(fw1.cget("text"))
        squad.append(fw2.cget("text"))
        squad.append(fw3.cget("text"))
        return(squad, default)

    def submitTeam():
        bank = budget_entry.get()
        # check budget is numeric and has a value
        if bank != "" and bank.isnumeric() == True:
            # clear transfer suggestion box
            transfer_list_box.delete(0, END)
            squad, default = getSquad()
            # check for alike items in lists
            result = set(squad).intersection(default)
            isEmpty = (result == set())
            if isEmpty:
                transfers = t.suggestTransfer(
                    squad, transfer.get(), int(float(bank)))
                for i in range(len(transfers)):
                    transfer_list_box.insert(END, transfers[i])

    # graph stats
    def graphData():
        squad, not_used = getSquad()
        squad_df = df.loc[df['name'].isin(squad)]
        team_data = squad_df[['name', selected_stat.get()]]
        fig = px.bar(team_data, x='name', y=selected_stat.get(),
                     color='name', title='Stats')
        fig.show()

    # undo action
    def undo():
        if players_added != []:
            player_to_remove = players_added[-1]
            if gk1.cget("text") == player_to_remove:
                gk1.config(text="GK")
            if gk2.cget("text") == player_to_remove:
                gk2.config(text="GK")
            if def1.cget("text") == player_to_remove:
                def1.config(text="Def")
            if def2.cget("text") == player_to_remove:
                def2.config(text="Def")
            if def3.cget("text") == player_to_remove:
                def3.config(text="Def")
            if def4.cget("text") == player_to_remove:
                def4.config(text="Def")
            if def5.cget("text") == player_to_remove:
                def5.config(text="Def")
            if mid1.cget("text") == player_to_remove:
                mid1.config(text="Mid")
            if mid2.cget("text") == player_to_remove:
                mid2.config(text="Mid")
            if mid3.cget("text") == player_to_remove:
                mid3.config(text="Mid")
            if mid4.cget("text") == player_to_remove:
                mid4.config(text="Mid")
            if mid5.cget("text") == player_to_remove:
                mid5.config(text="Mid")
            if fw1.cget("text") == player_to_remove:
                fw1.config(text="FW")
            if fw2.cget("text") == player_to_remove:
                fw2.config(text="FW")
            if fw2.cget("text") == player_to_remove:
                fw2.config(text="FW")
            players_added.pop()
            labels = getLabels(df)
            update(labels)

    def increase():
        # get current value
        bank_value = budget_entry.cget("text")
        # convert to float
        bank_value = float(bank_value)
        # increase value by 0.1
        bank_value += 0.1
        # prevent recurring floats
        bank_value = "{:.1f}".format(bank_value)
        # return new value
        budget_entry.config(text=bank_value)

    def decrease():
        if float(budget_entry.cget("text")) != 0.0:
            # get current value
            bank_value = budget_entry.cget("text")
            # convert to float
            bank_value = float(bank_value)
            # increase value by 0.1
            bank_value -= 0.1
            # prevent recurring floats
            bank_value = "{:.1f}".format(bank_value)
            # return new value
            budget_entry.config(text=bank_value)

    # GUI
    # init
    root = Tk()
    root.title('FPL analysis')
    root.config(bg='#B3D89C')
    root.geometry("1000x800")
    players_added = []

    # label
    search_label = Label(root, text="FPL Transfer Suggester",
                         fg='#4D7298', bg='#B3D89C', font=("Inter", 25))
    search_label.place(relx=.5, rely=0.05, anchor=CENTER)

    # starting XI labels
    # GKs
    gk1 = Label(root, text="GK", fg='#FFFFFF', bg='#9DC3C2', font=("Inter", 10), borderwidth=1,
                relief="solid", width=8, height=1, anchor=W)
    gk1.place(bordermode=INSIDE, relx=0.45, rely=0.3, anchor=CENTER)
    gk2 = Label(root, text="GK", fg='#FFFFFF', bg='#9DC3C2', font=("Inter", 10), borderwidth=1,
                relief="solid", width=8, height=1, anchor=W)
    gk2.place(bordermode=INSIDE, relx=0.55, rely=0.3, anchor=CENTER)
    # Defenders
    def1 = Label(root, text="Def", fg='#FFFFFF', bg='#9DC3C2', font=("Inter", 10), borderwidth=1,
                 relief="solid", width=8, height=1, anchor=W)
    def1.place(bordermode=INSIDE, relx=0.50, rely=0.4, anchor=CENTER)
    def2 = Label(root, text="Def", fg='#FFFFFF', bg='#9DC3C2', font=("Inter", 10), borderwidth=1,
                 relief="solid", width=8, height=1, anchor=W)
    def2.place(bordermode=INSIDE, relx=0.60, rely=0.4, anchor=CENTER)
    def3 = Label(root, text="Def", fg='#FFFFFF', bg='#9DC3C2', font=("Inter", 10), borderwidth=1,
                 relief="solid", width=8, height=1, anchor=W)
    def3.place(bordermode=INSIDE, relx=0.70, rely=0.4, anchor=CENTER)
    def4 = Label(root, text="Def", fg='#FFFFFF', bg='#9DC3C2', font=("Inter", 10), borderwidth=1,
                 relief="solid", width=8, height=1, anchor=W)
    def4.place(bordermode=INSIDE, relx=0.40, rely=0.4, anchor=CENTER)
    def5 = Label(root, text="Def", fg='#FFFFFF', bg='#9DC3C2', font=("Inter", 10), borderwidth=1,
                 relief="solid", width=8, height=1, anchor=W)
    def5.place(bordermode=INSIDE, relx=0.30, rely=0.4, anchor=CENTER)
    # Midfielders
    mid1 = Label(root, text="Mid", fg='#FFFFFF', bg='#9DC3C2', font=("Inter", 10), borderwidth=1,
                 relief="solid", width=8, height=1, anchor=W)
    mid1.place(bordermode=INSIDE, relx=0.50, rely=0.5, anchor=CENTER)
    mid2 = Label(root, text="Mid", fg='#FFFFFF', bg='#9DC3C2', font=("Inter", 10), borderwidth=1,
                 relief="solid", width=8, height=1, anchor=W)
    mid2.place(bordermode=INSIDE, relx=0.60, rely=0.5, anchor=CENTER)
    mid3 = Label(root, text="Mid", fg='#FFFFFF', bg='#9DC3C2', font=("Inter", 10), borderwidth=1,
                 relief="solid", width=8, height=1, anchor=W)
    mid3.place(bordermode=INSIDE, relx=0.70, rely=0.5, anchor=CENTER)
    mid4 = Label(root, text="Mid", fg='#FFFFFF', bg='#9DC3C2', font=("Inter", 10), borderwidth=1,
                 relief="solid", width=8, height=1, anchor=W)
    mid4.place(bordermode=INSIDE, relx=0.40, rely=0.5, anchor=CENTER)
    mid5 = Label(root, text="Mid", fg='#FFFFFF', bg='#9DC3C2', font=("Inter", 10), borderwidth=1,
                 relief="solid", width=8, height=1, anchor=W)
    mid5.place(bordermode=INSIDE, relx=0.30, rely=0.5, anchor=CENTER)
    # Forwards
    fw1 = Label(root, text="FW", fg='#FFFFFF', bg='#9DC3C2', font=("Inter", 10), borderwidth=1,
                relief="solid", width=8, height=1, anchor=W)
    fw1.place(bordermode=INSIDE, relx=0.50, rely=0.6, anchor=CENTER)
    fw2 = Label(root, text="FW", fg='#FFFFFF', bg='#9DC3C2', font=("Inter", 10), borderwidth=1,
                relief="solid", width=8, height=1, anchor=W)
    fw2.place(bordermode=INSIDE, relx=0.60, rely=0.6, anchor=CENTER)
    fw3 = Label(root, text="FW", fg='#FFFFFF', bg='#9DC3C2', font=("Inter", 10), borderwidth=1,
                relief="solid", width=8, height=1, anchor=W)
    fw3.place(bordermode=INSIDE, relx=0.40, rely=0.6, anchor=CENTER)

    # entry box
    search_player = Entry(root, width=100, fg='#FFFFFF',
                          bg='#77A6B6', font=("Inter", 10))
    search_player.place(relx=0.5, rely=0.1, anchor=CENTER)

    # budget label
    budget_entry = Label(root, width=10, text='0', fg='#FFFFFF',
                         bg='#77A6B6', font=("Inter", 10))
    budget_entry.place(relx=0.8, rely=.22, anchor=CENTER)

    # increment buttons
    increase_button = Button(root, width=1, text='+', fg='#FFFFFF',
                             bg='#84A6B1', font=("Inter", 10), command=increase)
    increase_button.place(relx=0.89, rely=.22, anchor=CENTER)

    decrease_button = Button(root, width=1, text='-', fg='#FFFFFF',
                             bg='#84A6B1', font=("Inter", 10), command=decrease)
    decrease_button.place(relx=0.86, rely=.22, anchor=CENTER)

    # free transfers input
    transfer = IntVar()
    transferBox = Checkbutton(
        root, text='Multi Transfer', font=("Inter", 10), variable=transfer, onvalue=1, offvalue=0, activebackground='#4D7298', selectcolor='#4D7298', fg='#FFFFFF')
    transferBox.config(bg='#4D7298')
    transferBox.place(relx=0.8, rely=0.29, anchor=CENTER)

    # list box
    player_search_list = Listbox(
        root, width=45, height=5, fg='#FFFFFF', bg='#84A6B1', font=("Inter", 10))
    player_search_list.place(relx=0.5, rely=0.2, anchor=CENTER)
    labels = getLabels(df)
    update(labels)

    # transfers list box
    transfer_list_box = Listbox(
        root, width=90, height=10, fg='#FFFFFF', bg='#84A6B1', font=("Inter", 10))
    transfer_list_box.place(relx=0.5, rely=0.82, anchor=CENTER)

    # confirm Button
    enter_button = Button(root, width=6, text="Confirm", fg='#FFFFFF',
                          bg='#4D7298', font=("Inter", 10), command=submit)
    enter_button.place(relx=.70, rely=.15, anchor=CENTER)

    # clear Button
    clear_button = Button(root, width=6, text="Clear", fg='#FFFFFF',
                          bg='#4D7298', font=("Inter", 10), command=clearLabels)
    clear_button.place(relx=.70, rely=.22, anchor=CENTER)

    # submit squad Button
    submit_button = Button(root, width=6, text="Submit", fg='#FFFFFF',
                           bg='#4D7298', font=("Inter", 10), command=submitTeam)
    submit_button.place(relx=.70, rely=.29, anchor=CENTER)

    # print selected item
    player_search_list.bind("<<ListboxSelect>>", fillout)
    search_player.bind("<KeyRelease>", check)

    # graphing
    # dropdownlist opitions
    stat_headings = ['minutes', 'goals_scored',
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
                     'ict_index_rank']
    # menu data type
    selected_stat = StringVar()
    # intial value
    selected_stat.set('goals_scored')
    # create dropdown list
    heading_select = OptionMenu(root, selected_stat, *stat_headings)
    heading_select.config(fg='#FFFFFF',
                          bg='#4D7298', font=("Inter", 10))
    heading_select["menu"].config(fg='#FFFFFF',
                                  bg='#4D7298', font=("Inter", 10))
    heading_select.place(relx=.10, rely=.75, anchor=CENTER)
    # graph button
    graph = Button(root, width=10, text="Graph Data", fg='#FFFFFF',
                   bg='#4D7298', font=("Inter", 10), command=graphData)
    graph.place(relx=.10, rely=.70, anchor=CENTER)

    # remove last action
    undo_button = Button(root, width=6, text="Undo", fg='#FFFFFF',
                         bg='#4D7298', font=("Inter", 10), command=undo)
    undo_button.place(relx=.8, rely=.15, anchor=CENTER)

    root.mainloop()


if __name__ == '__main__':
    display()
