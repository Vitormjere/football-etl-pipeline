# Football ETL Pipeline
 
A data pipeline that extracts football standings and match results from a public API, calculates team form and points percentage, stores historical snapshots, and generates a weekly PDF report, running automatically on a schedule.
 
## About the project
 
Built as a portfolio project to explore a different kind of problem than my C#/.NET projects: data extraction and transformation (ETL), instead of a request/response web API. The pipeline is split into isolated stages (extract, transform, load, report), with the transformation logic kept pure and dependency-free so it can be unit tested without hitting the API or the database.
 
## Tech stack
 
Python 3.13 · requests · python-dotenv · SQLite · fpdf2 · pytest · football-data.org API · Windows Task Scheduler
 
## Features
 
- Fetches standings and finished-match results for three competitions: Premier League, Champions League, and La Liga
- Calculates each team's recent form (last 5 games: win/draw/loss) and points percentage
- Stores a timestamped snapshot of every run in SQLite, enabling comparison of team performance over time
- Generates a formatted PDF report per run, with a Unicode-capable font (handles special characters in team names)
- Runs automatically every week via Windows Task Scheduler, with no manual step required
- Unit tests covering the transformation logic (match result calculation, form calculation, points percentage)
## Architecture
 
The pipeline follows a linear Extract → Transform → Load → Report flow, with each stage in its own module:
 
- `src/extract.py` - talks to the football-data.org API; returns raw JSON, no business logic
- `src/transform.py` - pure functions: match result per team, recent form, points percentage, team summaries. No API or database calls, which is what makes it unit-testable in isolation
- `src/load.py` - persists a snapshot of each run to a local SQLite database
- `src/report.py` - generates the PDF report from the transformed data
- `main.py` - orchestrates the full pipeline
- `tests/` - pytest unit tests for the transformation logic
## Running locally
 
**Prerequisites:** Python 3.13+, a free API key from [football-data.org](https://www.football-data.org/client/register)
 
```bash
git clone https://github.com/Vitormjere/football-etl-pipeline.git
cd football-etl-pipeline
py -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
 
Create a `.env` file in the project root:
```
FOOTBALL_DATA_API_KEY=your_token_here
```
 
Run the pipeline:
```bash
py main.py
```
 
This fetches the latest data, saves a snapshot to `pipeline.db`, and generates `relatorio.pdf` in the project root.
 
## Tests
 
```bash
pytest -v
```
 
Covers the transformation logic: match result calculation (win/draw/loss from a team's perspective), points percentage calculation, and recent-form ordering.
 
## Automation
 
The pipeline is configured to run automatically every Sunday via Windows Task Scheduler, executing `main.py` with the project's virtual environment, no manual intervention needed to keep the historical data and report up to date.
 
## Author
 
Vitor Miranda Jeremias — [GitHub](https://github.com/Vitormjere)
