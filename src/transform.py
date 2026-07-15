from src.extract import get_matches, get_standings

def get_match_result(match, team_id):
    winner = match["score"]["winner"]

    is_home = match["homeTeam"]["id"] == team_id

    if winner == "DRAW":
        return "E"
    elif winner == "HOME_TEAM" and is_home:
        return "V"
    elif winner == "AWAY_TEAM" and not is_home:
        return "V"
    else:
        return "D"

def get_team_form(matches, team_id, num_games=5):
    jogos_do_time = [
        m for m in matches
        if m["homeTeam"]["id"] == team_id or m["awayTeam"]["id"] == team_id
    ]

    jogos_ordenados = sorted(jogos_do_time, key=lambda m: m["utcDate"])

    ultimos_jogos = jogos_ordenados[-num_games:]

    forma = [get_match_result(m, team_id) for m in ultimos_jogos]

    return forma

def calcular_aproveitamento(forma):
    if len(forma) == 0:
        return 0.0

    pontos_por_resultado = {"V": 3, "E": 1, "D": 0}

    pontos_conquistados = sum(pontos_por_resultado[resultado] for resultado in forma)
    pontos_possiveis = len(forma) * 3

    aproveitamento = (pontos_conquistados / pontos_possiveis) * 100

    return round(aproveitamento, 1)

def build_team_summaries(standings_data, matches_data):
    partidas = matches_data["matches"]
    tabela = standings_data["standings"][0]["table"]

    resumos = []

    for time_na_tabela in tabela:
        team_id = time_na_tabela["team"]["id"]
        team_name = time_na_tabela["team"]["name"]

        forma = get_team_form(partidas, team_id)
        aproveitamento = calcular_aproveitamento(forma)

        resumo = {
            "time": team_name,
            "posicao": time_na_tabela["position"],
            "pontos": time_na_tabela["points"],
            "forma": forma,
            "aproveitamento": aproveitamento
        }

        resumos.append(resumo)

    return resumos

if __name__ == "__main__":
    standings = get_standings("PL", season="2025")
    dados_partidas = get_matches("PL", status="FINISHED", season="2025")

    resumos = build_team_summaries(standings, dados_partidas)

    for r in resumos:
        print(r)