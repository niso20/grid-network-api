import time
from datetime import datetime, date
import pytz

def convertTimeToTimestamp(time_str: str, date_str: str = None, timezone_str: str = None) -> float:
    """
    Convert time with specific date

    Args:
        time_str: Time string like "21:45:0"
        date_str: Date string like "2024-12-06" (optional, uses today if None)
    """
    time_parts = time_str.split(":")
    hours = int(time_parts[0])
    minutes = int(time_parts[1])
    seconds = int(time_parts[2]) if len(time_parts) > 2 else 0

    if date_str:
        # Parse date string
        date_parts = date_str.split("-")
        year = int(date_parts[0])
        month = int(date_parts[1])
        day = int(date_parts[2])
        dt = datetime(year, month, day, hours, minutes, seconds)
    else:
        # Use today's date
        today = date.today()
        dt = datetime.combine(today, datetime.min.time().replace(hour=hours, minute=minutes, second=seconds))

    # Handle timezone if specified
    if timezone_str:
        tz = pytz.timezone(timezone_str)
        dt = tz.localize(dt)

    # Convert to Unix timestamp
    return dt.timestamp()