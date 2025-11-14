CONFIG = {
    "max_retries": 3,
    "backoff_base": 2
}

def set_config(key, value):
    CONFIG[key] = value

def get_config(key):
    return CONFIG.get(key)
