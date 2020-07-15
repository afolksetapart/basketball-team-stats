import constants
import copy
import textwrap
import statistics
import sys

TEAMS = constants.TEAMS
PLAYERS = constants.PLAYERS


def clean_data():
    """Makes a copy of and cleans PLAYERS data from any file 
    formatted like constants.py

    Returns:
        List: A list of dictionaries containing clean player data
    """
    data_copy = copy.deepcopy(PLAYERS)
    for player in data_copy:
        player['height'] = int(player['height'][:2])
        player['guardians'] = player['guardians'].split(" and ")
        if player['experience'] == "YES":
            player['experience'] = True
        else:
            player['experience'] = False
    return data_copy


def balance_teams(clean_data):
    """Evenly sorts players into experienced, inexperienced lists 
    (if possible, else sys.exit()) and calls populate_teams()
    passing lists as arguments with return value stored in 
    full_teams and then passed to format_teams()

    Args:
        clean_data (list): Clean player data from any file 
        formatted like constants.py

    Returns:
        Dict: Output of format_teams(full_teams) as 
        dict with team name as key and team players 
        (list of dicts) as value 
    """
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
    """Determines even number of players per team (else calls 
    sys.exit()) and distributes even number of experienced, 
    inexperienced players to each team list

    Args:
        exp_list (list): List of experienced players as dicts
        inexp_list (list): List of inexperienced players as dicts

    Returns:
        List: A list containing multiple lists of player dicts for 
        each team
    """
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
    """For each team, assigns team name from constants.py as 
    key to dict, assigns value as list containing player dicts

    Args:
        teams (list): List containing lists of player dicts

    Returns:
        Dict: A dict with each team name as a key, and list 
        of players dicts for that team as value
    """
    team_names_copy = TEAMS.copy()
    teams_dict = {key: value for key, value in zip(team_names_copy, teams)}
    return teams_dict


def get_team_name(selection):
    """Gets team name based on user selection from teams menu

    Args:
        selection (int): User selection from teams menu

    Returns:
        String: Team name
    """
    return TEAMS[(selection - 1)]


def display_stats(selection):
    """Formats and displays stats for any team in teamns manu
    based on user input

    Args:
        selection (int): User selection from teams menu
    """
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
    """Calls clean_data() followed by balance_teams() (passing in
    the return of clean_data() as argument)

    Returns:
        Dict: A dict containing populated and sorted teams
    """
    clean_player_data = clean_data()
    teams_data = balance_teams(clean_player_data)
    return teams_data


def check_value(value, condition):
    """Converts user input to int, checks that user inputed a 
    valid selection from current menu, else raises ValueError 
    and prompts for valid selection

    Args:
        value (string): User selection from menu
        condition (int): Length of menu

    Returns:
        Int: User selection from menu
    """
    while True:
        try:
            value = int(value)
            if value > condition or value <= 0:
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
