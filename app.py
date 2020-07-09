import constants
import copy
import textwrap
import statistics
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
            f"""Unbalanced experience among players: 
            You currently have {len(experienced)} experienced players and {len(inexperienced)} inexperienced players.
            Please adjust roster.""")
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
        return teams
    else:
        sys.exit(
            f"""Uneven number of players per team ({round(players_per_team, 1)}):
            Please adjust roster.""")


def format_teams(teams):
    team_names_copy = TEAMS.copy()
    teams_dict = {key: value for key, value in zip(team_names_copy, teams)}
    return teams_dict


def get_team_name(selection):
    return TEAMS[(selection - 1)]


def display_stats(selection):
    team_name = get_team_name(selection)
    team = new_teams[team_name]
    avg_height = statistics.mean([player['height'] for player in team])

    print("Players: \n")
    for player in team:
        guardians = ", ".join(player['guardians'])
        print(f"{player['name']}\n  [Guardians: {guardians}]")
    print(f"\nTotal Players: {len(team)}")
    print(
        f"Total Experienced: {len([player for player in team if player['experience'] == True])}")
    print(
        f"Total Inexperienced: {len([player for player in team if player['experience'] == False])}")
    print(f"Average Height: {round(avg_height, 1)} inches")


def start_program():
    clean_player_data = clean_data()
    teams_data = balance_teams(clean_player_data)
    return teams_data


def check_value(value, condition):
    while True:
        try:
            value = int(value)
            if value > condition:
                raise ValueError
            break
        except ValueError:
            value = input(
                f"\nError: Please enter a valid selection from the menu above >  ")
            continue
    return value


if __name__ == "__main__":
    new_teams = start_program()

    print(textwrap.dedent("""
    ***BASKETBALL TEAM ASSIGNMENT & STATS TOOL***

    [All players have been successfuly assigned to a team]
    """))

    while True:
        print(textwrap.dedent("""
        -\/\/\/- MENU -\/\/\/-

        1 Display Team Stats 

        2 Quit
        """))

        main_menu_selection = input("Please select from the above menu >  ")
        main_menu_selection = check_value(main_menu_selection, 2)

        if main_menu_selection == 1:
            print(textwrap.dedent(""" 
            -\/\/\/- TEAMS -\/\/\/-
            """))

            i = 1
            for team in TEAMS:
                print(textwrap.dedent(f"""
                {i} {team}"""))
                if (i == len(TEAMS)):
                    print("\n")
                    break
                i += 1

            sub_menu_selection = input("Please select a team >  ")
            sub_menu_selection = check_value(sub_menu_selection, len(TEAMS))

            print(textwrap.dedent(f""" 
            -\/\/\/- {get_team_name(sub_menu_selection).upper()} STATS -\/\/\/-
            """))

            display_stats(sub_menu_selection)

            input("\nPress Enter to continue...")

        if main_menu_selection == 2:
            sys.exit()
