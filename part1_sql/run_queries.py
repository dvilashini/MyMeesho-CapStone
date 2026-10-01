import sqlite3
import subprocess
import os

DB_PATH = os.path.join("data", "meesho_reseller.db")
SQL_PATH = os.path.join("Part1_SQL", "queries.sql")

def run_queries():
    # Use sqlite3 CLI to execute queries.sql
    subprocess.run(["sqlite3", DB_PATH, ".read " + SQL_PATH], shell=True)

if __name__ == "__main__":
    run_queries()
    print("Queries executed. CSV outputs written to Part1_SQL/output/")
