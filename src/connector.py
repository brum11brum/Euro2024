from src import db_operations
from datetime import datetime


def fetch_teams() -> list[str]:
    return db_operations.teams_list()


def add_new_game_to_db(home_team, away_team, date):
    db_operations.insert_game(home_team, away_team, date)


def check_missing() -> list[tuple]:
    all_null = db_operations.grab_null()
    date_today = datetime.now().date()
    results = []
    for item in all_null:
        year, month, day = [int(x) for x in item[3].split('-')]
        item_date = datetime(year, month, day).date()
        if item_date <= date_today:
            results.append(item)
    return results


def new_predicition(
        name: str,
        home_goals: str,
        away_goals: str,
        home_team: str,
        away_team: str,
        stage: int,
        event=None
) -> str:
    result = f"{home_goals}-{away_goals}"
    game_id = db_operations.get_game_id(home_team, away_team)
    if not game_id:
        return f'No such game {home_team}-{away_team} by {name}'
    db_operations.add_prediction(name, game_id, result, stage)
    return f'added {home_team}-{away_team} by {name}'


def update_old_game(home_team: str, away_team: str, home_goals: str, away_goals: str) -> None:
    if not home_goals or not away_goals:
        return
    result = f"{home_goals}-{away_goals}"
    db_operations.update_game(home_team, away_team, result)


def show_winner(home: int, away: int) -> str:
    if home == away:
        return 'draw'
    if home < away:
        return 'away'
    if home > away:
        return 'home'
    return 'dk'


def compare_results(predicted: str, actual: str) -> tuple[bool, str, str]:
    predicted_home, predicted_away = [int(x) for x in predicted.split('-')]
    predicted_win = show_winner(predicted_home, predicted_away)
    actual_home, actual_away = [int(x) for x in actual.split('-')]
    actual_win = show_winner(actual_home, actual_away)
    if predicted_win == actual_win:
        return True, predicted_win, actual_win
    return False, predicted_win, actual_win


def show_results(name: str, stage: list[str]) -> tuple[list[tuple], dict]:
    results: list = []
    additional_stats: dict = {
        'hits': {'home': 0, 'away': 0, 'draw': 0,'exact_result': 0},
        'miss': {'home': 0, 'away': 0, 'draw': 0, 'exact_result': 0}
    }
    predictions = db_operations.get_predictions(name)
    for prediction in predictions:
        if str(prediction[4]) not in stage:
            continue
        predicted_result = prediction[3]
        actual_from_db = db_operations.get_game_by_id(prediction[2])
        actual_result = actual_from_db[4]
        if not actual_result:
            continue
        if predicted_result == actual_result:
            additional_stats['hits']['exact_result'] += 1
        else:
            additional_stats['miss']['exact_result'] += 1
        hit, predicted_win, actual_win = compare_results(predicted_result, actual_result)
        if hit:
            additional_stats['hits'][predicted_win] += 1
        else:
            additional_stats['miss'][predicted_win] += 1
        game = f"{actual_from_db[1]}-{actual_from_db[2]}"
        record = game, predicted_result, actual_result, hit
        results.append(record)
    return results, additional_stats
