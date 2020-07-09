import constants
import copy
import sys

TEAMS = constants.TEAMS
PLAYERS = constants.PLAYERS


def clean_data():
    data_copy = PLAYERS.copy()
    for player in data_copy:
        player['height'] = int(player['height'][:2])
        player['guardians'] = player['guardians'].split(" and ")
        if player['experience'] == "YES":
            player['experience'] = True
        else:
            player['experience'] = False
    return data_copy


def balance_teams(clean_data):
    experienced = [
        player for player in clean_data if player['experience'] == True]
    inexperienced = [
        player for player in clean_data if player['experience'] == False]
    if len(experienced) != len(inexperienced):
        sys.exit(
            f"Unbalanced experience among players.\nYou currently have {len(experienced)} experienced players and {len(inexperienced)} inexperienced players.\nPlease adjust roster.")
    else:
        full_teams = populate_teams(experienced, inexperienced)
        return format_teams(full_teams)


def populate_teams(exp_list, inexp_list):
    num_players = len(PLAYERS)
    num_teams = len(TEAMS)
    players_per_team = (num_players/num_teams)

    if (num_players % num_teams == 0):
        teams = []
        int(players_per_team)
        for team_name in TEAMS:
            teams.append([])
        for team in teams:
            while len(team) < players_per_team:
                team.append(exp_list.pop())
                team.append(inexp_list.pop())
        print(num_players % num_teams)
        return teams
    else:
        sys.exit(
            f"Uneven number of players per team({round(players_per_team, 1)}), unable to distribute evenly. Please adjust roster.")


def format_teams(teams):
    team_names_copy = TEAMS.copy()
    teams_dict = {key: value for key, value in zip(team_names_copy, teams)}
    return teams_dict


def display_player_names(team):
    print(f"{TEAMS[(team -1)]}")
    for player in team:
        print(f"\n{player['name']}")


def start_program():
    clean_player_data = clean_data()
    teams_data = balance_teams(clean_player_data)
    return teams_data


if __name__ == "__main__":
    new_teams = start_program()

    print("""
    ***BASKETBALL TEAM ASSIGNMENT & STATS TOOL***

    [All players have been successfuly assigned to a team]
    """)

    while True:
        print("""
        -\/\/\/- MENU -\/\/\/-

        1 Display Team Stats 
        2 Quit

        """)

        main_menu_selection = int(
            input("Please select from the above menu >  "))

        if main_menu_selection == 1:
            print(""" 
            -\/\/\/- TEAMS -\/\/\/-
            """)

            i = 1
            for team in TEAMS:
                print(f"""{i} {team}""")
                if (i == len(TEAMS)):
                    print("\n")
                    break
                i += 1

            sub_menu_selection = int(
                input("Please select a team >  "))

            display_player_names()

        if main_menu_selection == 2:
            sys.exit()
