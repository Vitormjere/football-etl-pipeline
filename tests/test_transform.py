import pytest
from src.transform import get_match_result, calcular_aproveitamento, get_team_form

def test_get_match_result_vitoria_mandante():
    match = {
        "homeTeam": {"id": 1},
        "awayTeam": {"id": 2},
        "score": {"winner": "HOME_TEAM"}
    }

    resultado = get_match_result(match, team_id=1)

    assert resultado == "V"


def test_get_match_result_derrota_mandante():
    match = {
        "homeTeam": {"id": 1},
        "awayTeam": {"id": 2},
        "score": {"winner": "AWAY_TEAM"}
    }

    resultado = get_match_result(match, team_id=1)

    assert resultado == "D"


def test_get_match_result_vitoria_visitante():
    match = {
        "homeTeam": {"id": 1},
        "awayTeam": {"id": 2},
        "score": {"winner": "AWAY_TEAM"}
    }

    resultado = get_match_result(match, team_id=2)

    assert resultado == "V"


def test_get_match_result_empate():
    match = {
        "homeTeam": {"id": 1},
        "awayTeam": {"id": 2},
        "score": {"winner": "DRAW"}
    }

    resultado = get_match_result(match, team_id=1)

    assert resultado == "E"


@pytest.mark.parametrize("forma, esperado", [
    ([], 0.0),
    (["V", "V", "V"], 100.0),
    (["D", "D", "D"], 0.0),
    (["V", "D"], 50.0),
    (["V", "E", "D"], 44.4),
])
def test_calcular_aproveitamento(forma, esperado):
    resultado = calcular_aproveitamento(forma)

    assert resultado == esperado


def test_get_team_form_retorna_ultimos_5_em_ordem():
    matches = [
        {"utcDate": "2026-01-05", "homeTeam": {"id": 1}, "awayTeam": {"id": 2}, "score": {"winner": "HOME_TEAM"}},
        {"utcDate": "2026-01-01", "homeTeam": {"id": 1}, "awayTeam": {"id": 3}, "score": {"winner": "AWAY_TEAM"}},
        {"utcDate": "2026-01-03", "homeTeam": {"id": 4}, "awayTeam": {"id": 1}, "score": {"winner": "DRAW"}},
    ]

    forma = get_team_form(matches, team_id=1, num_games=5)

    assert forma == ["D", "E", "V"]