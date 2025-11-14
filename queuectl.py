import click
from queue_manager import enqueue_job, get_jobs_by_state, list_dlq, retry_dlq
from worker import start_workers, stop_workers
from utils import generate_job_id
from db import init_db
from config import set_config

init_db()

@click.group()
def cli():
    pass

@cli.command()
@click.argument("job_json")
def enqueue(job_json):
    import json
    job = json.loads(job_json)
    if "id" not in job:
        job["id"] = generate_job_id()
    enqueue_job(job)
    click.echo(f"Enqueued job {job['id']}")

@cli.group()
def worker():
    pass

@worker.command("start")
@click.option("--count", default=1, help="Number of workers")
def start(count):
    start_workers(count)
    click.echo(f"Started {count} worker(s)")

@worker.command("stop")
def stop():
    stop_workers()
    click.echo("Stopped all workers")

@cli.command()
def status():
    states = ["pending", "processing", "completed", "failed", "dead"]
    for s in states:
        jobs = get_jobs_by_state(s)
        click.echo(f"{s}: {len(jobs)} jobs")

@cli.command()
@click.option("--state", default=None)
def list(state):
    if state:
        jobs = get_jobs_by_state(state)
    else:
        jobs = get_jobs_by_state("pending") + get_jobs_by_state("processing") + get_jobs_by_state("completed") + get_jobs_by_state("failed") + get_jobs_by_state("dead")
    for job in jobs:
        click.echo(job)

@cli.group()
def dlq():
    pass

@dlq.command("list")
def dlq_list():
    jobs = list_dlq()
    for job in jobs:
        click.echo(job)

@dlq.command("retry")
@click.argument("job_id")
def dlq_retry(job_id):
    retry_dlq(job_id)
    click.echo(f"Retried job {job_id} from DLQ")

@cli.group()
def config():
    pass

@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key, value):
    try:
        value = int(value)
    except:
        pass
    set_config(key, value)
    click.echo(f"Config {key} set to {value}")

if __name__ == "__main__":
    cli()
