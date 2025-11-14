import subprocess
import time
import json

# Enqueue jobs
subprocess.run(['python', 'queuectl.py', 'enqueue', '{"command":"echo Hello"}'])
subprocess.run(['python', 'queuectl.py', 'enqueue', '{"command":"exit 1"}'])
subprocess.run(['python', 'queuectl.py', 'enqueue', '{"command":"sleep 2"}'])

# Start workers
subprocess.Popen(['python', 'queuectl.py', 'worker', 'start', '--count', '2'])

# Wait for jobs to finish
time.sleep(10)

# Check status
subprocess.run(['python', 'queuectl.py', 'status'])

# List DLQ
subprocess.run(['python', 'queuectl.py', 'dlq', 'list'])
