import threading
import subprocess
import time
from queue_manager import get_jobs_by_state, update_job_state, move_to_dlq
from config import get_config

WORKERS = []
WORKER_RUNNING = True

def worker_loop(worker_id):
    while WORKER_RUNNING:
        jobs = get_jobs_by_state("pending")
        if not jobs:
            time.sleep(1)
            continue
        for job in jobs:
            job_id, command, state, attempts, max_retries, created_at, updated_at = job
            update_job_state(job_id, "processing")
            try:
                result = subprocess.run(command, shell=True)
                if result.returncode == 0:
                    update_job_state(job_id, "completed")
                else:
                    handle_failure(job, attempts + 1)
            except Exception:
                handle_failure(job, attempts + 1)
        time.sleep(0.5)

def handle_failure(job, attempts):
    job_id = job[0]
    max_retries = job[4]
    if attempts > max_retries:
        update_job_state(job_id, "dead")
        move_to_dlq({
            "id": job_id,
            "command": job[1],
            "state": "dead",
            "attempts": attempts,
            "max_retries": max_retries,
            "created_at": job[5]
        })
    else:
        update_job_state(job_id, "failed", attempts)
        delay = get_config("backoff_base") ** attempts
        time.sleep(delay)

def start_workers(count):
    global WORKERS, WORKER_RUNNING
    WORKER_RUNNING = True
    for i in range(count):
        t = threading.Thread(target=worker_loop, args=(i,))
        t.start()
        WORKERS.append(t)

def stop_workers():
    global WORKER_RUNNING
    WORKER_RUNNING = False
    for t in WORKERS:
        t.join()
