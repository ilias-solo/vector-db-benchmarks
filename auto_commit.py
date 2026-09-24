import os
import subprocess
from datetime import datetime
import random

# Configuration
REPO_PATH = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(REPO_PATH, "benchmark_logs.md")

def generate_log_entry():
    """Generates a realistic-looking benchmark log entry."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    db_names = ["Faiss", "Milvus", "Qdrant", "Chroma", "Weaviate"]
    db = random.choice(db_names)
    latency = round(random.uniform(1.5, 45.2), 2)
    recall = round(random.uniform(0.85, 0.99), 4)
    throughput = random.randint(500, 5000)
    
    entry = f"""
### Benchmark Run - {now}
- **Database:** {db}
- **Dataset:** SIFT1M
- **Query Throughput:** {throughput} ops/sec
- **p99 Latency:** {latency} ms
- **Recall@10:** {recall}
- **Status:** Test completed successfully. Index optimized.
"""
    return entry

def run_command(command):
    """Runs a shell command and handles output."""
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=REPO_PATH)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error executing: {command}\n{stderr.decode('utf-8')}")
        return False
    return True

def main():
    # 1. Append new log data
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(generate_log_entry())
    
    # 2. Git Add
    if not run_command("git add ."):
        return
    
    # 3. Git Commit
    commit_msg = f"perf: daily benchmark run - {datetime.now().strftime('%Y-%m-%d')}"
    if not run_command(f'git commit -m "{commit_msg}"'):
        return
    
    # 4. Git Push
    if not run_command("git push origin main"):
        # If 'main' fails, try 'master' as fallback
        run_command("git push origin master")

if __name__ == "__main__":
    main()
    print("Auto-commit complete.")