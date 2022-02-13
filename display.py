# imports
from tkinter import *
import FPLCompleteData as fpl
import cProfile
import pstats
import FPLtransfers as t


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
        transfer_list_box

    def submitTeam():
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
        # check for alike items in lists
        result = set(squad).intersection(default)
        isEmpty = (result == set())
        if isEmpty:
            transfers = t.suggestTransfer(squad, 2)
            for i in range(len(transfers)):
                transfer_list_box.insert(END, transfers[i])

    # GUI
    # init
    root = Tk()
    root.title('FPL analysis')
    root.geometry("1000x800")

    # label
    search_label = Label(root, text="Search Player")
    search_label.place(relx=.5, rely=0.05, anchor=CENTER)

    # starting XI labels
    # GKs
    gk1 = Label(root, text="GK", borderwidth=1,
                relief="solid", width=8, height=1)
    gk1.place(bordermode=INSIDE, relx=0.45, rely=0.3, anchor=CENTER)
    gk2 = Label(root, text="GK", borderwidth=1,
                relief="solid", width=8, height=1)
    gk2.place(bordermode=INSIDE, relx=0.55, rely=0.3, anchor=CENTER)
    # Defenders
    def1 = Label(root, text="Def", borderwidth=1,
                 relief="solid", width=8, height=1)
    def1.place(bordermode=INSIDE, relx=0.50, rely=0.4, anchor=CENTER)
    def2 = Label(root, text="Def", borderwidth=1,
                 relief="solid", width=8, height=1)
    def2.place(bordermode=INSIDE, relx=0.60, rely=0.4, anchor=CENTER)
    def3 = Label(root, text="Def", borderwidth=1,
                 relief="solid", width=8, height=1)
    def3.place(bordermode=INSIDE, relx=0.70, rely=0.4, anchor=CENTER)
    def4 = Label(root, text="Def", borderwidth=1,
                 relief="solid", width=8, height=1)
    def4.place(bordermode=INSIDE, relx=0.40, rely=0.4, anchor=CENTER)
    def5 = Label(root, text="Def", borderwidth=1,
                 relief="solid", width=8, height=1)
    def5.place(bordermode=INSIDE, relx=0.30, rely=0.4, anchor=CENTER)
    # Midfielders
    mid1 = Label(root, text="Mid", borderwidth=1,
                 relief="solid", width=8, height=1)
    mid1.place(bordermode=INSIDE, relx=0.50, rely=0.5, anchor=CENTER)
    mid2 = Label(root, text="Mid", borderwidth=1,
                 relief="solid", width=8, height=1)
    mid2.place(bordermode=INSIDE, relx=0.60, rely=0.5, anchor=CENTER)
    mid3 = Label(root, text="Mid", borderwidth=1,
                 relief="solid", width=8, height=1)
    mid3.place(bordermode=INSIDE, relx=0.70, rely=0.5, anchor=CENTER)
    mid4 = Label(root, text="Mid", borderwidth=1,
                 relief="solid", width=8, height=1)
    mid4.place(bordermode=INSIDE, relx=0.40, rely=0.5, anchor=CENTER)
    mid5 = Label(root, text="Mid", borderwidth=1,
                 relief="solid", width=8, height=1)
    mid5.place(bordermode=INSIDE, relx=0.30, rely=0.5, anchor=CENTER)
    # Forwards
    fw1 = Label(root, text="FW", borderwidth=1,
                relief="solid", width=8, height=1)
    fw1.place(bordermode=INSIDE, relx=0.50, rely=0.6, anchor=CENTER)
    fw2 = Label(root, text="FW", borderwidth=1,
                relief="solid", width=8, height=1)
    fw2.place(bordermode=INSIDE, relx=0.60, rely=0.6, anchor=CENTER)
    fw3 = Label(root, text="FW", borderwidth=1,
                relief="solid", width=8, height=1)
    fw3.place(bordermode=INSIDE, relx=0.40, rely=0.6, anchor=CENTER)

    # entry box
    search_player = Entry(root, width=100)
    search_player.place(relx=0.5, rely=0.1, anchor=CENTER)

    # list box
    player_search_list = Listbox(root, width=50, height=5)
    player_search_list.place(relx=0.5, rely=0.2, anchor=CENTER)
    labels = getLabels(df)
    update(labels)

    # transfers list box
    transfer_list_box = Listbox(root, width=100, height=10)
    transfer_list_box.place(relx=0.5, rely=0.82, anchor=CENTER)

    # confirm Button
    enter_button = Button(root, width=6, text="Confirm", command=submit)
    enter_button.place(relx=.78, rely=.15, anchor=CENTER)

    # clear Button
    clear_button = Button(root, width=6, text="Clear", command=clearLabels)
    clear_button.place(relx=.78, rely=.22, anchor=CENTER)

    # submit squad Button
    submit_button = Button(root, width=6, text="Submit", command=submitTeam)
    submit_button.place(relx=.78, rely=.29, anchor=CENTER)

    # print selected item
    player_search_list.bind("<<ListboxSelect>>", fillout)
    search_player.bind("<KeyRelease>", check)

    root.mainloop()


display()
