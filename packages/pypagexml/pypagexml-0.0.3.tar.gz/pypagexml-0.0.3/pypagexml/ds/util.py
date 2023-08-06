def iso_now():
    from datetime import datetime
    return datetime.utcnow().isoformat(timespec='seconds')
