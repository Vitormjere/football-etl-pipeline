from fpdf import FPDF, XPos, YPos
from datetime import datetime

NOMES_LIGAS = {
    "PL": "Premier League",
    "CL": "Champions League",
    "PD": "La Liga"
}

def generate_report(dados, output_path="relatorio.pdf"):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Relatorio Semanal de Futebol", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.set_font("Helvetica", "", 10)
    data_geracao = datetime.now().strftime("%d/%m/%Y %H:%M")
    pdf.cell(0, 8, f"Gerado em: {data_geracao}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.ln(5)

    for codigo, times in dados.items():
        nome_liga = NOMES_LIGAS.get(codigo, codigo)

        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, nome_liga, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)

        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(10, 8, "Pos", border=1)
        pdf.cell(70, 8, "Time", border=1)
        pdf.cell(20, 8, "Pontos", border=1)
        pdf.cell(30, 8, "Aprov.", border=1)
        pdf.cell(40, 8, "Forma", border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.set_font("Helvetica", "", 9)
        for time in times:
            forma_texto = " ".join(time["forma"])

            pdf.cell(10, 8, str(time["posicao"]), border=1)
            pdf.cell(70, 8, time["time"], border=1)
            pdf.cell(20, 8, str(time["pontos"]), border=1)
            pdf.cell(30, 8, f"{time['aproveitamento']}%", border=1)
            pdf.cell(40, 8, forma_texto, border=1, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        pdf.ln(8)

    pdf.output(output_path)

if __name__ == "__main__":
    from src.extract import get_standings, get_matches
    from src.transform import build_team_summaries

    standings = get_standings("PL", season="2025")
    matches = get_matches("PL", status="FINISHED", season="2025")
    resumos = build_team_summaries(standings, matches)

    print(f"Quantidade de times: {len(resumos)}")

    generate_report({"PL": resumos}, "relatorio.pdf")
    print("Relatorio gerado!")