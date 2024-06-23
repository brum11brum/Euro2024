import sqlite3
from os import path as pathos

from datetime import datetime


predictions_path = pathos.join(pathos.split(pathos.dirname(__file__))[0], 'db', 'predictions.db')


def insert_game(
        home_team: str,
        away_team: str,
        date: str,
) -> str:

    con = sqlite3.connect(predictions_path)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO games (home_team, away_team, date) VALUES(?, ?, ?);",
        (home_team, away_team, date)
    )
    con.commit()
    con.close()
    return f"Game {home_team}-{away_team} played on {date} created!"


def update_game(
        home_team: str,
        away_team: str,
        result: str,
        extra_time: str = 'No',
        penalties: str = 'No'
) -> str:
    con = sqlite3.connect(predictions_path)
    cur = con.cursor()
    cur.execute(
        f"UPDATE games SET result = ?, extra_time = ?, penalties = ? WHERE home_team = ? AND away_team = ?",
        (result, extra_time, penalties, home_team, away_team)
    )
    con.commit()
    con.close()


def add_prediction(
        name: str,
        game: str,
        result: str,
        stage: int
) -> str:
    con = sqlite3.connect(predictions_path)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO predictions (name, game, result, stage) VALUES(?, ?, ?, ?);",
        (name, game, result, stage)
    )
    con.commit()
    con.close()


def teams_list() -> list[str]:
    con = sqlite3.connect(predictions_path)
    cur = con.cursor()
    res = cur.execute("SELECT home_team FROM games")
    result = {x[0] for x in res.fetchall()}
    return sorted(list(result))


def grab_null() -> list[tuple]:
    con = sqlite3.connect(predictions_path)
    cur = con.cursor()
    res = cur.execute("SELECT * FROM games WHERE result IS NULL")
    result = res.fetchall()
    return result
    # result = {x[0] for x in res.fetchall()}


def get_game_id(home_team: str, away_team: str) -> int:
    con = sqlite3.connect(predictions_path)
    cur = con.cursor()
    res = cur.execute(
        "SELECT * FROM games WHERE home_team = ? AND away_team = ?", (home_team, away_team)
    )
    result = res.fetchone()
    con.close()
    if result:
        return result[0]
    return 0


def get_game_by_id(game_id: int) -> tuple:
    con = sqlite3.connect(predictions_path)
    cur = con.cursor()
    res = cur.execute(
        "SELECT * FROM games WHERE id = ?", (game_id,)
    )
    result = res.fetchone()
    con.close()
    return result


def get_predictions(name: str) -> list[tuple]:
    con = sqlite3.connect(predictions_path)
    cur = con.cursor()
    if name == 'Both':
        res = cur.execute(
            "SELECT * FROM predictions "
        )
    else:
        res = cur.execute(
            "SELECT * FROM predictions WHERE name=?", (name,)
        )
    result = res.fetchall()
    con.close()
    return result


def check_predicitons_db():
    if pathos.isfile(predictions_path):
        return
    # if database doesn't exist, create one along with two tables: predictions and games
    con = sqlite3.connect(predictions_path)
    cur = con.cursor()
    cur.executescript('''
    CREATE TABLE predictions (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name    TEXT,
        game    INTEGER,
        result  TEXT,
        stage   INTEGER
    );
    CREATE TABLE games (
        id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        home_team   TEXT,
        away_team   TEXT,
        date    DATE,
        result  TEXT,
        extra_time  TEXT,
        penalties   TEXT
    )
    ''')
    con.close()
