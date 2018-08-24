from datetime import datetime as dt, timezone as tz
# general utils
def time_type(start, end):
    """Gives the time type for a given start and end time.
    Returns "past", "present" or "future". start and end should be datetimes or FancyTimes.
    """
    start = getattr(start, "dt", start)
    end = getattr(end, "dt", end)
    now = dt.now(tz.utc)
    if end < start:
        raise ValueError("end was after start")
    if now <= start:
        return "future"
    elif start < now <= end:
        return "present"
    elif end < now:
        return "past"
    else:
        # :thonk:
        raise ValueError("I'm not sure how this happened because this should be impossible")
