import re
import calendar
from datetime import datetime, timedelta


def parse_smart_date(date_str: str, base_date: datetime | None = None) -> datetime:
    if base_date is None:
        base_date = datetime.now()

    s = date_str.lower().strip()

    # 1. YYYY-MM-DD HH:MM
    m = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{2})$", s)
    if m:
        y, mo, d, h, mi = map(int, m.groups())
        return datetime(y, mo, d, h, mi)

    # 2. YYYY-MM-DD
    m = re.match(r"^(\d{4})-(\d{1,2})-(\d{1,2})$", s)
    if m:
        y, mo, d = map(int, m.groups())
        return datetime(y, mo, d, base_date.hour, base_date.minute)

    # 3. MM-DD HH:MM
    m = re.match(r"^(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{2})$", s)
    if m:
        mo, d, h, mi = map(int, m.groups())
        try:
            dt = datetime(base_date.year, mo, d, h, mi)
            if dt < base_date:
                dt = dt.replace(year=base_date.year + 1)
            return dt
        except ValueError:
            return datetime(base_date.year + 1, mo, d, h, mi)

    # 4. MM-DD
    m = re.match(r"^(\d{1,2})-(\d{1,2})$", s)
    if m:
        mo, d = map(int, m.groups())
        try:
            dt = datetime(base_date.year, mo, d, base_date.hour, base_date.minute)
            if dt < base_date:
                dt = dt.replace(year=base_date.year + 1)
            return dt
        except ValueError:
            return datetime(base_date.year + 1, mo, d, base_date.hour, base_date.minute)

    # 5. DD HH:MM
    m = re.match(r"^(\d{1,2})\s+(\d{1,2}):(\d{2})$", s)
    if m:
        d, h, mi = map(int, m.groups())
        curr_y, curr_m = base_date.year, base_date.month

        # Check current month
        try:
            dt = datetime(curr_y, curr_m, d, h, mi)
            if dt >= base_date:
                return dt
        except ValueError:
            pass

        next_m = curr_m + 1
        next_y = curr_y
        if next_m > 12:
            next_m = 1
            next_y += 1

        return datetime(next_y, next_m, d, h, mi)

    # 6. DD HH (Day + Hour, 00 min inferred)
    m = re.match(r"^(\d{1,2})\s+(\d{1,2})$", s)
    if m:
        d, h = map(int, m.groups())
        mi = 0

        curr_y, curr_m = base_date.year, base_date.month

        try:
            dt = datetime(curr_y, curr_m, d, h, mi)
            if dt >= base_date:
                return dt
        except ValueError:
            pass

        next_m = curr_m + 1
        next_y = curr_y
        if next_m > 12:
            next_m = 1
            next_y += 1

        return datetime(next_y, next_m, d, h, mi)

    # 6.5 Month Names (Feb 14 21:00, Feb 14)
    months_map = {}
    for i in range(1, 13):
        months_map[calendar.month_abbr[i].lower()] = i
        months_map[calendar.month_name[i].lower()] = i

    parts = s.split()
    if parts and parts[0] in months_map:
        mo = months_map[parts[0]]

        if len(parts) > 1 and parts[1].isdigit():
            d = int(parts[1])

            h, mi = base_date.hour, base_date.minute
            if len(parts) > 2:
                tm = re.match(r"^(\d{1,2}):(\d{2})$", parts[2])
                if tm:
                    h, mi = map(int, tm.groups())
                else:
                    if parts[2].isdigit():
                        h = int(parts[2])
                        mi = 0

            try:
                dt = datetime(base_date.year, mo, d, h, mi)
                if dt < base_date:
                    dt = dt.replace(year=base_date.year + 1)
                return dt
            except ValueError:
                return datetime(base_date.year + 1, mo, d, h, mi)

    # 7. Weekdays
    weekdays = {
        "mon": 0,
        "monday": 0,
        "tue": 1,
        "tuesday": 1,
        "wed": 2,
        "wednesday": 2,
        "thu": 3,
        "thursday": 3,
        "fri": 4,
        "friday": 4,
        "sat": 5,
        "saturday": 5,
        "sun": 6,
        "sunday": 6,
    }

    parts = s.split()
    if parts:
        wd_str = parts[0]
        if wd_str in weekdays:
            target_weekday = weekdays[wd_str]

            h, mi = base_date.hour, base_date.minute

            if len(parts) > 1:
                t_str = parts[1]
                tm = re.match(r"^(\d{1,2}):(\d{2})$", t_str)
                if tm:
                    h, mi = map(int, tm.groups())
                else:
                    tm = re.match(r"^(\d{1,2})$", t_str)
                    if tm:
                        h = int(tm.group(1))
                        mi = 0

            current_weekday = base_date.weekday()
            days_ahead = target_weekday - current_weekday

            candidate_date = base_date.date() + timedelta(days=days_ahead)
            candidate_dt = datetime.combine(
                candidate_date, datetime.min.time()
            ).replace(hour=h, minute=mi)

            if days_ahead < 0:
                candidate_dt += timedelta(days=7)
            elif days_ahead == 0:
                if candidate_dt < base_date:
                    candidate_dt += timedelta(days=7)

            return candidate_dt

    # 10. Time Only (HH:MM or HH)
    m = re.match(r"^(\d{1,2}):(\d{2})$", s)
    if m:
        h, mi = map(int, m.groups())
        dt = datetime(base_date.year, base_date.month, base_date.day, h, mi)
        if dt < base_date:
            dt += timedelta(days=1)
        return dt

    # HH
    m = re.match(r"^(\d{1,2})$", s)
    if m:
        h = int(m.group(1))
        if 0 <= h <= 23:
            dt = datetime(base_date.year, base_date.month, base_date.day, h, 0)
            if dt < base_date:
                dt += timedelta(days=1)
            return dt

    raise ValueError(f"Could not parse date: {date_str}")
