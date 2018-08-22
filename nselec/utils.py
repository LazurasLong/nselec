from datetime import datetime as dt, timezone as tz
# general utils
def time_type(start, end):
    """Gives the time type for a given start and end time.
    Returns "past", "present" or "future". start and end should be datetimes.
    """
    now = dt.now(tz.utc)
    if end < start:
        raise ValueError("end was after start")
    if now <= start:
        return "past"
    elif start < now <= end:
        return "present"
    elif end < now:
        return "future"
    else:
        # :thonk:
        raise ValueError("I'm not sure how this happened because this should be impossible")
