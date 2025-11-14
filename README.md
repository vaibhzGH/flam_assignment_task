# QueueCTL - Background Job Queue CLI

## Overview

`queuectl` is a **Python-based CLI tool** for managing background jobs with support for:

* Multiple worker processes
* Retry failed jobs with **exponential backoff**
* Dead Letter Queue (DLQ) for permanently failed jobs
* Persistent job storage using SQLite
* Configurable retry and backoff settings

It allows developers to enqueue jobs, monitor workers, and manage failed jobs—all from the terminal.

---

## Features

* Enqueue shell commands as jobs
* Concurrent workers with thread-based processing
* Retry mechanism with exponential backoff (`delay = base^attempts`)
* Dead Letter Queue for jobs that fail after max retries
* Persistent storage using SQLite (`jobs.db`)
* CLI commands for job management, DLQ handling, and configuration

---

## Project Structure

```
queuectl/
│
├─ queuectl.py          # Main CLI entry point
├─ queue_manager.py     # Job queue & DLQ management
├─ worker.py            # Worker threads & job execution
├─ db.py                # SQLite DB wrapper
├─ config.py            # Configuration management (retry, backoff)
├─ utils.py             # Helper functions (UUID, timestamps)
├─ tests.py             # Test script for core flows
├─ README.md            # This file
└─ requirements.txt     # Python dependencies
```

---

## Job Lifecycle

| State        | Description                             |
| ------------ | --------------------------------------- |
| `pending`    | Waiting to be picked up by a worker     |
| `processing` | Currently being executed                |
| `completed`  | Successfully executed                   |
| `failed`     | Failed, but retryable                   |
| `dead`       | Permanently failed and moved to **DLQ** |

**Flow:**

```
pending → processing → completed
          ↘ failed → retry → completed / dead → DLQ
```

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/vaibhzGH/flam_assignment_task.git
cd queuectl
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

> `sqlite3` comes with Python ≥3.6, so only `click` is required.

---

## CLI Usage

### Enqueue a Job

```bash
python queuectl.py enqueue '{"command":"echo Hello"}'
```

### Start Workers

```bash
python queuectl.py worker start --count 2
```

### Stop Workers

```bash
python queuectl.py worker stop
```

### Check Job Status

```bash
python queuectl.py status
```

### List Jobs by State

```bash
python queuectl.py list --state pending
```

### Dead Letter Queue (DLQ)

* List all DLQ jobs:

```bash
python queuectl.py dlq list
```

* Retry a DLQ job:

```bash
python queuectl.py dlq retry <job_id>
```

### Configuration

* Set maximum retries or backoff base:

```bash
python queuectl.py config set max_retries 5
python queuectl.py config set backoff_base 3
```

---

## Testing

`tests.py` includes **basic test scenarios**:

1. Enqueue successful and failing jobs
2. Start multiple workers
3. Verify retry mechanism
4. Check DLQ operations

Run the test script:

```bash
python tests.py
```

---

## Architecture Overview

* **queuectl.py** – CLI entry point using `click`
* **queue_manager.py** – Handles job operations, state updates, DLQ movement
* **worker.py** – Runs worker threads, executes jobs, manages retries/backoff
* **db.py** – SQLite database wrapper for persistent storage
* **config.py** – Configurable retry count and backoff base
* **utils.py** – Helper functions for generating job IDs and timestamps
* **tests.py** – Test script to validate core functionality

**Key Points:**

* Workers pick up only `pending` jobs
* Each job execution checks the **exit code**
* Failed jobs are retried automatically
* Jobs exceeding max retries are moved to DLQ
* Persistent storage ensures jobs survive system restarts

---

## Assumptions & Trade-offs

* SQLite is used for simplicity (not distributed)
* Workers are threads (lightweight, not multiprocessing)
* Commands executed via shell; success determined by exit code
* Exponential backoff: `delay = base ^ attempts` (configurable base)
* Minimal CLI, no web dashboard or priority queues (optional bonus features)

---

## Example Flow

1. Enqueue jobs:

```bash
python queuectl.py enqueue '{"command":"sleep 2"}'
python queuectl.py enqueue '{"command":"exit 1"}'
```

2. Start 2 workers:

```bash
python queuectl.py worker start --count 2
```

3. Check job status:

```bash
python queuectl.py status
```

4. Failed jobs move to DLQ after max retries:

```bash
python queuectl.py dlq list
```

5. Retry jobs from DLQ:

```bash
python queuectl.py dlq retry <job_id>
```

---

## Notes

* Jobs and DLQ are stored in **`jobs.db`**
* You can configure retries and backoff via CLI
* Graceful shutdown ensures workers finish current job before stopping

---

This README includes **setup, usage, architecture, job lifecycle, testing, and assumptions** for the QueueCTL project.
