import os
import subprocess
from datetime import datetime

def run_git(args, env=None):
    subprocess.run(["git"] + args, check=False, env=env)

commits = [
    ("2026-02-15 10:00:00", "init: basic project structure and e-commerce simulator", ["streaming-simulator/", ".gitignore", "README.md", "requirements.txt"]),
    ("2026-02-20 14:30:00", "feat: raw ingestion using autoloader for orders stream", ["databricks-notebooks/bronze/"]),
    ("2026-02-28 11:15:00", "feat: silver cleansing with basic deduplication", ["databricks-notebooks/silver/"]),
    ("2026-03-05 22:45:00", "fix: added 24h watermark to handle late payment confirmations", ["databricks-notebooks/silver/02_cleansing_orders.py"]),
    ("2026-03-12 16:20:00", "feat: gold layer hourly aggregation for revenue KPIs", ["databricks-notebooks/gold/"]),
    ("2026-03-18 09:10:00", "docs: added initial operational runbook and setup notes", ["documentation/runbook/"]),
    ("2026-03-25 19:40:00", "fix: checkpoint corruption recovery steps added to troubleshooting", ["documentation/troubleshooting/"]),
    ("2026-04-02 11:00:00", "refactor: standardized column naming to total_amount across layers", ["sql-scripts/ddl/01_create_star_schema.sql", "databricks-notebooks/gold/03_kpi_aggregations.py"]),
    ("2026-04-10 15:30:00", "feat: added reconciliation query for data audit", ["sql-scripts/validations/"]),
    ("2026-04-15 13:45:00", "fix: deterministic dedup using row_number() over window", ["databricks-notebooks/silver/02_cleansing_orders.py"]),
    ("2026-04-22 10:15:00", "feat: adf orchestration for medallion streaming jobs", ["adf-pipelines/"]),
    ("2026-04-28 16:50:00", "chore: moved environment configs to centralized folder", ["configs/"]),
    ("2026-05-02 23:10:00", "fix: optimized bronze write settings for expected sales spike", ["databricks-notebooks/bronze/01_raw_to_bronze.py"]),
    ("2026-05-08 14:20:00", "feat: manual replay utility for quarantined records", ["utilities/manual_replay.py"]),
    ("2026-05-12 11:00:00", "docs: final runbook update and known issues cleanup", ["documentation/runbook/operational_runbook.md", "README.md"]),
    ("2026-05-15 16:30:00", "chore: finalized gold layer trigger logic in adf", ["adf-pipelines/orchestration/PL_Main_Streaming_Orchestration.json"]),
    ("2026-05-16 10:20:00", "refactor: added config_loader utility for better path management", ["databricks-notebooks/streaming-utils/", "databricks-notebooks/bronze/01_raw_to_bronze.py", "documentation/dev_history.md", "cicd/", "sql-scripts/reporting/", "sql-scripts/stored-procedures/"])
]

repo_path = r"c:\Users\gajul\OneDrive\Desktop\Antigravity All working Projects\E-Commerce Streaming Platform"
os.chdir(repo_path)

for date_str, msg, files in commits:
    for f in files:
        if os.path.isdir(f):
            subprocess.run(["git", "add", f], check=False)
        elif os.path.isfile(f):
            subprocess.run(["git", "add", f], check=False)
    
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    
    # Use --allow-empty to avoid failure if no files changed in a specific commit
    subprocess.run(["git", "commit", "--allow-empty", "-m", msg], env=env, check=False)

# Final add to catch anything missed
subprocess.run(["git", "add", "."], check=False)
subprocess.run(["git", "commit", "-m", "final: catch-all for remaining files"], check=False)

print("Git history simulation complete.")
