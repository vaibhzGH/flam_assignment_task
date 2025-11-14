from db import execute
from utils import current_time
from config import get_config

def enqueue_job(job):
    job.setdefault("state", "pending")
    job.setdefault("attempts", 0)
    job.setdefault("max_retries", get_config("max_retries"))
    job.setdefault("created_at", current_time())
    job.setdefault("updated_at", current_time())
    
    query = '''INSERT INTO jobs (id, command, state, attempts, max_retries, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)'''
    execute(query, (job["id"], job["command"], job["state"], job["attempts"],
                    job["max_retries"], job["created_at"], job["updated_at"]))

def get_jobs_by_state(state):
    return execute("SELECT * FROM jobs WHERE state=?", (state,), fetch=True)

def update_job_state(job_id, state, attempts=None):
    updated_at = current_time()
    if attempts is not None:
        execute("UPDATE jobs SET state=?, attempts=?, updated_at=? WHERE id=?",
                (state, attempts, updated_at, job_id))
    else:
        execute("UPDATE jobs SET state=?, updated_at=? WHERE id=?",
                (state, updated_at, job_id))

def move_to_dlq(job):
    execute('''
        INSERT OR REPLACE INTO dlq (id, command, last_state, attempts, max_retries, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (job["id"], job["command"], job["state"], job["attempts"], job["max_retries"], job["created_at"], current_time()))
    execute("DELETE FROM jobs WHERE id=?", (job["id"],))

def list_dlq():
    return execute("SELECT * FROM dlq", fetch=True)

def retry_dlq(job_id):
    job = execute("SELECT * FROM dlq WHERE id=?", (job_id,), fetch=True)
    if job:
        job = job[0]
        enqueue_job({
            "id": job[0],
            "command": job[1],
            "state": "pending",
            "attempts": 0,
            "max_retries": job[4],
            "created_at": job[5]
        })
        execute("DELETE FROM dlq WHERE id=?", (job_id,))
