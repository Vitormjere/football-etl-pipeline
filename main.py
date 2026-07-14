from src.extract import get_standings, get_matches
from src.transform import build_team_summaries
from src.load import init_db, save_snapshot
from src.report import generate_report

COMPETICOES = ["PL", "CL", "PD"]
TEMPORADA = "2025"

def run_pipeline():
    init_db()

    resultado_geral = {}

    for codigo in COMPETICOES:
        standings = get_standings(codigo, season=TEMPORADA)
        matches = get_matches(codigo, status="FINISHED", season=TEMPORADA)

        resumos = build_team_summaries(standings, matches)

        save_snapshot(codigo, resumos)

        resultado_geral[codigo] = resumos

    return resultado_geral

if __name__ == "__main__":
    dados = run_pipeline()

    generate_report(dados, "relatorio.pdf")

    print("Pipeline executado, dados salvos e relatorio gerado!")