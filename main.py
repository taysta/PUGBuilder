from itertools import combinations, permutations
from typing import List, Tuple
import logging

# Define constants
NUM_OFFENSE_NEEDED = 3
NUM_CHASE_NEEDED = 1
NUM_HOME_NEEDED = 1
RATING_TOLERANCE = 100
TEAM_SIZE = NUM_OFFENSE_NEEDED + NUM_CHASE_NEEDED + NUM_HOME_NEEDED


class Player:
    def __init__(self, user_id=0, username="", rating=0, position=""):
        self.rating = rating
        self.username = username
        self.user_id = user_id
        self.position = position


def generate_match_combinations(players: List[Player]) -> List[Tuple[Tuple[Player, ...], Tuple[Player, ...]]]:
    logging.info("Generating balanced matches for %d players.", len(players))

    offense_players = [player for player in players if player.position in ('offense', 'flexible')]
    chase_players = [player for player in players if player.position in ('chase', 'flexible')]
    home_players = [player for player in players if player.position in ('home', 'flexible')]

    players.sort(key=lambda player: player.rating, reverse=True)

    balanced_matches = []

    offense_permutations = permutations(offense_players, NUM_OFFENSE_NEEDED)
    chase_permutations = permutations(chase_players, NUM_CHASE_NEEDED)
    home_permutations = permutations(home_players, NUM_HOME_NEEDED)

    for team1_offense in offense_permutations:
        for team1_chase in chase_permutations:
            for team1_home in home_permutations:
                team1 = team1_offense + team1_chase + team1_home
                remaining_players = list(set(players) - set(team1))

                if len(remaining_players) >= TEAM_SIZE:
                    team2_offense = generate_team_by_position(remaining_players, NUM_OFFENSE_NEEDED,
                                                              ('offense', 'flexible'))
                    team2_chase = generate_team_by_position(remaining_players, NUM_CHASE_NEEDED, ('chase', 'flexible'))
                    team2_home = generate_team_by_position(remaining_players, NUM_HOME_NEEDED, ('home', 'flexible'))

                    team2 = team2_offense + team2_chase + team2_home

                    if len(team1) == TEAM_SIZE and len(team2) == TEAM_SIZE:
                        match = (team1, team2)
                        tolerance = calculate_tolerance(match)
                        if is_balanced_match(tolerance, RATING_TOLERANCE):
                            balanced_matches.append(match)

    if not balanced_matches:
        logging.warning("No balanced matches with the current player positions. Trying to use rating instead.")
        balanced_matches = generate_balanced_matches_by_rating(players, NUM_OFFENSE_NEEDED)

    if not balanced_matches:
        logging.warning("No balanced matches found. Providing the 12 best unbalanced options instead.")
        unbalanced_matches = generate_unbalanced_matches(players)
        return sorted(unbalanced_matches, key=lambda unbalanced_match: calculate_tolerance(unbalanced_match))[:12]

    return sorted(balanced_matches, key=lambda balanced_match: calculate_tolerance(balanced_match))


def calculate_tolerance(match):
    team1_ratings = [player.rating for player in match[0]]
    team2_ratings = [player.rating for player in match[1]]

    average_rating_team1 = sum(team1_ratings) / len(team1_ratings)
    average_rating_team2 = sum(team2_ratings) / len(team2_ratings)

    return abs(average_rating_team1 - average_rating_team2)


def is_balanced_match(tolerance, rating_tolerance):
    return tolerance <= rating_tolerance


def generate_team_by_position(remaining_players, num_needed, positions):
    team = []
    for player in remaining_players:
        if player.position in positions and len(team) < num_needed:
            team.append(player)
    return team


def generate_balanced_matches_by_rating(players, rating_tolerance):
    balanced_matches = []
    for team1 in combinations(players, TEAM_SIZE):
        remaining_players = list(set(players) - set(team1))
        for team2 in combinations(remaining_players, TEAM_SIZE):
            if len(team1) == TEAM_SIZE and len(team2) == TEAM_SIZE:
                match = (team1, team2)
                tolerance = calculate_tolerance(match)
                if is_balanced_match(tolerance, rating_tolerance):
                    balanced_matches.append(match)
    return balanced_matches


def generate_unbalanced_matches(players):
    unbalanced_matches = []
    for team1 in combinations(players, TEAM_SIZE):
        remaining_players = list(set(players) - set(team1))
        for team2 in combinations(remaining_players, TEAM_SIZE):
            if len(team1) == TEAM_SIZE and len(team2) == TEAM_SIZE:
                match = (team1, team2)
                unbalanced_matches.append(match)
    return unbalanced_matches
