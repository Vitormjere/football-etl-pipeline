import sqlite3
from datetime import datetime

DB_PATH = "pipeline.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            execution_date TEXT NOT NULL,
            competition_code TEXT NOT NULL,
            team_name TEXT NOT NULL,
            position INTEGER,
            points INTEGER,
            aproveitamento REAL,
            forma TEXT
        )
    """)

    conn.commit()
    conn.close()

def save_snapshot(competition_code, team_summaries):
    conn = get_connection()
    cursor = conn.cursor()

    execution_date = datetime.now().isoformat()

    for time in team_summaries:
        forma_como_texto = ",".join(time["forma"])

        cursor.execute("""
            INSERT INTO team_snapshots
                (execution_date, competition_code, team_name, position, points, aproveitamento, forma)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            execution_date,
            competition_code,
            time["time"],
            time["posicao"],
            time["pontos"],
            time["aproveitamento"],
            forma_como_texto
        ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Banco inicializado com sucesso!")