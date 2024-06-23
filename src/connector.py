from src import db_operations
from datetime import datetime


def fetch_teams() -> list[str]:
    return db_operations.teams_list()


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


def compare_results(predicted: str, actual: str) -> bool:
    predicted_home, predicted_away = [int(x) for x in predicted.split('-')]
    predicted_win = show_winner(predicted_home, predicted_away)
    actual_home, actual_away = [int(x) for x in actual.split('-')]
    actual_win = show_winner(actual_home, actual_away)
    if predicted_win == actual_win:
        return True
    return False


def show_results(name: str, stage: list[str]) -> list[tuple]:
    results: list = []
    predictions = db_operations.get_predictions(name)
    for prediction in predictions:
        if str(prediction[4]) not in stage:
            continue
        predicted_result = prediction[3]
        actual_from_db = db_operations.get_game_by_id(prediction[2])
        actual_result = actual_from_db[4]
        if not actual_result:
            continue
        hit = compare_results(predicted_result, actual_result)
        game = f"{actual_from_db[1]}-{actual_from_db[2]}"
        record = game, predicted_result, actual_result, hit
        results.append(record)
    return results



if __name__ == '__main__':

    data = [
        ('Gronkjer', '2', '0', 'Germany', 'Scotland', '1'),
        ('Gronkjer', '1', '1', 'Hungary', 'Switzerland', '1'),
        ('Gronkjer', '3', '0', 'Spain', 'Croatia', '1'),
        ('Gronkjer', '3', '1', 'Italy', 'Albania', '1'),
        ('Gronkjer', '0', '2', 'Slovenia', 'Denmark', '1'),
        ('Gronkjer', '0', '3', 'Serbia', 'England', '1'),
        ('Gronkjer', '2', '1', 'Poland', 'Netherlands', '1'),
        ('Gronkjer', '1', '1', 'Austria', 'France', '1'),
        ('Gronkjer', '1', '1', 'Belgium', 'Slovakia', '1'),
        ('Gronkjer', '1', '1', 'Romania', 'Ukraine', '1'),
        ('Gronkjer', '2', '1', 'Turkiye', 'Georgia', '1'),
        ('Gronkjer', '3', '0', 'Portugal', 'Czechia', '1'),
        ('Gronkjer', '2', '0', 'Germany', 'Hungary', '2'),
        ('Gronkjer', '1', '1', 'Scotland', 'Switzerland', '2'),
        ('Gronkjer', '2', '2', 'Spain', 'Italy', '2'),
        ('Gronkjer', '3', '1', 'Croatia', 'Albania', '2'),
        ('Gronkjer', '1', '1', 'Slovenia', 'Serbia', '2'),
        ('Gronkjer', '1', '2', 'Denmark', 'England', '2'),
        ('Gronkjer', '0', '3', 'Netherlands', 'France', '2'),
        ('Gronkjer', '2', '1', 'Poland', 'Austria', '2'),
        ('Gronkjer', '1', '2', 'Slovakia', 'Ukraine', '2'),
        ('Gronkjer', '2', '0', 'Belgium', 'Romania', '2'),
        ('Gronkjer', '0', '2', 'Georgia', 'Czechia', '2'),
        ('Gronkjer', '1', '4', 'Turkiye', 'Portugal', '2'),
        ('Gronkjer', '2', '1', 'Switzerland', 'Germany', '3'),
        ('Gronkjer', '2', '1', 'Scotland', 'Hungary', '3'),
        ('Gronkjer', '0', '4', 'Albania', 'Spain', '3'),
        ('Gronkjer', '2', '2', 'Croatia', 'Italy', '3'),
        ('Gronkjer', '3', '1', 'England', 'Slovenia', '3'),
        ('Gronkjer', '2', '0', 'Denmark', 'Serbia', '3'),
        ('Gronkjer', '1', '1', 'Netherlands', 'Austria', '3'),
        ('Gronkjer', '4', '1', 'France', 'Poland', '3'),
        ('Gronkjer', '0', '3', 'Ukraine', 'Belgium', '3'),
        ('Gronkjer', '1', '1', 'Slovakia', 'Romania', '3'),
        ('Gronkjer', '1', '3', 'Czechia', 'Turkiye', '3'),
        ('Gronkjer', '1', '3', 'Georgia', 'Portugal', '3'),
        ('El Comentarista', '2', '1', 'Germany', 'Scotland', '1'),
        ('El Comentarista', '0', '1', 'Hungary', 'Switzerland', '1'),
        ('El Comentarista', '1', '1', 'Spain', 'Croatia', '1'),
        ('El Comentarista', '1', '1', 'Italy', 'Albania', '1'),
        ('El Comentarista', '0', '2', 'Slovenia', 'Denmark', '1'),
        ('El Comentarista', '1', '1', 'Serbia', 'England', '1'),
        ('El Comentarista', '2', '4', 'Poland', 'Netherlands', '1'),
        ('El Comentarista', '1', '2', 'Austria', 'France', '1'),
        ('El Comentarista', '3', '1', 'Belgium', 'Slovakia', '1'),
        ('El Comentarista', '1', '2', 'Romania', 'Ukraine', '1'),
        ('El Comentarista', '3', '1', 'Turkiye', 'Georgia', '1'),
        ('El Comentarista', '2', '1', 'Portugal', 'Czechia', '1'),
        ('El Comentarista', '3', '1', 'Germany', 'Hungary', '2'),
        ('El Comentarista', '0', '3', 'Scotland', 'Switzerland', '2'),
        ('El Comentarista', '1', '1', 'Spain', 'Italy', '2'),
        ('El Comentarista', '3', '1', 'Croatia', 'Albania', '2'),
        ('El Comentarista', '0', '2', 'Slovenia', 'Serbia', '2'),
        ('El Comentarista', '1', '3', 'Denmark', 'England', '2'),
        ('El Comentarista', '2', '2', 'Netherlands', 'France', '2'),
        ('El Comentarista', '2', '1', 'Poland', 'Austria', '2'),
        ('El Comentarista', '1', '1', 'Slovakia', 'Ukraine', '2'),
        ('El Comentarista', '2', '1', 'Belgium', 'Romania', '2'),
        ('El Comentarista', '1', '3', 'Georgia', 'Czechia', '2'),
        ('El Comentarista', '2', '3', 'Turkiye', 'Portugal', '2'),
        ('El Comentarista', '2', '1', 'Switzerland', 'Germany', '3'),
        ('El Comentarista', '1', '3', 'Scotland', 'Hungary', '3'),
        ('El Comentarista', '0', '3', 'Albania', 'Spain', '3'),
        ('El Comentarista', '1', '1', 'Croatia', 'Italy', '3'),
        ('El Comentarista', '2', '0', 'England', 'Slovenia', '3'),
        ('El Comentarista', '2', '2', 'Denmark', 'Serbia', '3'),
        ('El Comentarista', '1', '1', 'Netherlands', 'Austria', '3'),
        ('El Comentarista', '3', '1', 'France', 'Poland', '3'),
        ('El Comentarista', '1', '2', 'Ukraine', 'Belgium', '3'),
        ('El Comentarista', '1', '2', 'Slovakia', 'Romania', '3'),
        ('El Comentarista', '2', '1', 'Czechia', 'Turkiye', '3'),
        ('El Comentarista', '1', '3', 'Georgia', 'Portugal', '3'),
    ]
    # for record in data:
    #     print(new_predicition(*record))
