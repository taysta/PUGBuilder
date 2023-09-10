import pytest
from main import (generate_match_combinations, Player, calculate_tolerance,
                  is_balanced_match, RATING_TOLERANCE, TEAM_SIZE)


@pytest.fixture
def sample_players():
    # Define some sample players with user_id, username, rating, and position
    return [
        Player(1, 'Player1', 1500, 'offense'),
        Player(2, 'Player2', 1600, 'chase'),
        Player(3, 'Player3', 1400, 'home'),
        Player(4, 'Player4', 1550, 'flexible'),
        Player(5, 'Player5', 1520, 'flexible'),
        Player(6, 'Player6', 1450, 'flexible'),
        Player(7, 'Player7', 1620, 'offense'),
        Player(8, 'Player8', 1580, 'chase'),
        Player(9, 'Player9', 1500, 'home'),
        Player(10, 'Player10', 1650, 'offense'),
    ]


@pytest.fixture
def sample_players_all_offense():
    # Define sample players with all players in "offense" position
    return [
        Player(1, 'Player1', 1500, 'offense'),
        Player(2, 'Player2', 1600, 'offense'),
        Player(3, 'Player3', 1400, 'offense'),
        Player(4, 'Player4', 1550, 'offense'),
        Player(5, 'Player5', 1520, 'offense'),
        Player(6, 'Player6', 1450, 'offense'),
        Player(7, 'Player7', 1620, 'offense'),
        Player(8, 'Player8', 1580, 'offense'),
        Player(9, 'Player9', 1500, 'offense'),
        Player(10, 'Player10', 1650, 'offense'),
    ]


@pytest.fixture
def sample_players_all_flexible():
    # Define sample players with all players in "flexible" position
    return [
        Player(1, 'Player1', 1500, 'flexible'),
        Player(2, 'Player2', 1600, 'flexible'),
        Player(3, 'Player3', 1400, 'flexible'),
        Player(4, 'Player4', 1550, 'flexible'),
        Player(5, 'Player5', 1520, 'flexible'),
        Player(6, 'Player6', 1450, 'flexible'),
        Player(7, 'Player7', 1620, 'flexible'),
        Player(8, 'Player8', 1580, 'flexible'),
        Player(9, 'Player9', 1500, 'flexible'),
        Player(10, 'Player10', 1650, 'flexible'),
    ]


@pytest.fixture
def sample_players_all_offense_extreme_ratings():
    # Define sample players with all players in "offense" position and extreme variance in ratings
    return [
        Player(1, 'Player1', 1000, 'offense'),
        Player(2, 'Player2', 3000, 'offense'),
        Player(3, 'Player3', 500, 'offense'),
        Player(4, 'Player4', 4000, 'offense'),
        Player(5, 'Player5', 800, 'offense'),
        Player(6, 'Player6', 4500, 'offense'),
        Player(7, 'Player7', 600, 'offense'),
        Player(8, 'Player8', 3500, 'offense'),
        Player(9, 'Player9', 200, 'offense'),
        Player(10, 'Player10', 5500, 'offense'),
    ]


@pytest.fixture
def sample_players_extreme_ratings():
    # Define sample players with extreme variance in ratings
    return [
        Player(1, 'Player1', 1500, 'offense'),
        Player(2, 'Player2', 1600, 'offense'),
        Player(3, 'Player3', 1400, 'offense'),
        Player(4, 'Player4', 2500, 'offense'),  # Extreme rating
        Player(5, 'Player5', 1000, 'offense'),  # Extreme rating
        Player(6, 'Player6', 1450, 'offense'),
        Player(7, 'Player7', 1620, 'offense'),
        Player(8, 'Player8', 1580, 'offense'),
        Player(9, 'Player9', 2000, 'offense'),  # Extreme rating
        Player(10, 'Player10', 1650, 'offense'),
    ]


def test_generate_match_combinations_with_all_offense(sample_players):
    # Modify the positions of players 4, 5, and 6 to be "offense"
    for player in sample_players[3:6]:
        player.position = "offense"

    matches = generate_match_combinations(sample_players)

    # Assert that there are matches in the result
    assert len(matches) > 0

    # Check if each match has exactly 2 teams with TEAM_SIZE players each
    for match in matches:
        assert len(match) == 2
        team1, team2 = match
        assert len(team1) == TEAM_SIZE
        assert len(team2) == TEAM_SIZE


def test_generate_match_combinations_with_all_flexible(sample_players):
    # Modify the positions of all players to be "flexible"
    for player in sample_players:
        player.position = "flexible"

    matches = generate_match_combinations(sample_players)

    # Assert that there are matches in the result
    assert len(matches) > 0

    # Check if each match has exactly 2 teams with TEAM_SIZE players each
    for match in matches:
        assert len(match) == 2
        team1, team2 = match
        assert len(team1) == TEAM_SIZE
        assert len(team2) == TEAM_SIZE


# Import statements and fixture definitions here...

# Test case for no players provided
def test_generate_match_combinations_no_players():
    """
    Test a scenario with no players provided.
    """
    empty_players = []
    matches = generate_match_combinations(empty_players)
    # Assert that there are no matches in the result
    assert len(matches) == 0


# Test case for exactly 10 players
def test_generate_match_combinations_exact_10_players(sample_players):
    """
    Test a scenario with exactly 10 players provided.
    """
    matches = generate_match_combinations(sample_players)
    # Assert that there are matches in the result
    assert len(matches) > 0


# Test case with exactly 10 players all in offense position
def test_generate_match_combinations_10_players_all_offense(sample_players_all_offense):
    """
    Test a scenario with exactly 10 players, all in "offense" position.
    """
    matches = generate_match_combinations(sample_players_all_offense)
    # Assert that there are matches in the result
    assert len(matches) > 0


# Test case with exactly 10 players all in flexible position
def test_generate_match_combinations_10_players_all_flexible(sample_players_all_flexible):
    """
    Test a scenario with exactly 10 players, all in "flexible" position.
    """
    matches = generate_match_combinations(sample_players_all_flexible)
    # Assert that there are matches in the result
    assert len(matches) > 0


# Test case with exactly 10 players in offense position and extreme ratings
def test_generate_match_combinations_10_players_all_offense_extreme_ratings(sample_players_all_offense_extreme_ratings):
    """
    Test a scenario with exactly 10 players in "offense" position with extreme ratings.
    """
    matches = generate_match_combinations(sample_players_all_offense_extreme_ratings)
    # Assert that there are no balanced matches in the result
    assert len(matches) > 0


# Test case with exactly 10 players with extreme ratings
def test_generate_match_combinations_10_players_extreme_ratings(sample_players_extreme_ratings):
    """
    Test a scenario with exactly 10 players with extreme ratings.
    """
    matches = generate_match_combinations(sample_players_extreme_ratings)
    # Assert that there are no balanced matches in the result
    assert len(matches) > 0


def test_generate_match_combinations_all_offense_extreme_ratings(sample_players_all_offense_extreme_ratings):
    """
    Test a scenario with exactly 10 players, all in "offense" position with extreme ratings.
    """
    matches = generate_match_combinations(sample_players_all_offense_extreme_ratings)

    # Assert that there are matches in the result
    assert len(matches) > 0

    # Check if each match has exactly 2 teams with TEAM_SIZE players each
    for match in matches:
        assert len(match) == 2
        team1, team2 = match
        assert len(team1) == TEAM_SIZE
        assert len(team2) == TEAM_SIZE

    # Check that the matches are balanced based on ratings
    for match in matches:
        tolerance = calculate_tolerance(match)
        assert is_balanced_match(tolerance, RATING_TOLERANCE)


# End of test cases
