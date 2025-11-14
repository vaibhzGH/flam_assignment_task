import uuid
from datetime import datetime

def generate_job_id():
    return str(uuid.uuid4())

def current_time():
    return datetime.utcnow().isoformat()
