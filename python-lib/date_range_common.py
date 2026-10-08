from datetime import datetime, timedelta


DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.000Z"


def _parse_date(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("{} is required.".format(label))
    value = value.strip()
    if value.endswith("Z"):
        value = value[:-1]
    for date_format in ("%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"):
        try:
            return datetime.strptime(value, date_format)
        except ValueError:
            pass
    raise ValueError("{} must use YYYY-MM-DDTHH:MM:SS.000Z format.".format(label))


def get_date_range(config, now=None):
    date_range = config.get("date_range")
    if date_range in (None, "custom", "manual"):
        prefix = "manual_" if date_range == "manual" else ""
        start = _parse_date(config.get(prefix + "start_date"), "Start date")
        end = _parse_date(config.get(prefix + "end_date"), "End date")
        if start > end:
            raise ValueError("Start date must be on or before end date.")
        return (
            start.isoformat(timespec="milliseconds"),
            end.isoformat(timespec="milliseconds"),
        )

    today = now if now is not None else datetime.now()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    rolling_days = {
        "last_7_days": 7,
        "last_14_days": 14,
        "last_30_days": 30,
        "last_60_days": 60,
    }
    if date_range == "today":
        start = end = today
    elif date_range == "yesterday":
        start = end = today - timedelta(days=1)
    elif date_range in rolling_days:
        start = today - timedelta(days=rolling_days[date_range])
        end = today - timedelta(days=1)
    elif date_range in ("last_work_week", "last_week"):
        start = today - timedelta(days=today.weekday() + 7)
        end = start + timedelta(days=4 if date_range == "last_work_week" else 6)
    elif date_range == "last_month":
        end = today.replace(day=1) - timedelta(days=1)
        start = end.replace(day=1)
    elif date_range == "last_quarter":
        current_quarter_start = today.replace(
            month=((today.month - 1) // 3) * 3 + 1, day=1
        )
        end = current_quarter_start - timedelta(days=1)
        start = end.replace(month=((end.month - 1) // 3) * 3 + 1, day=1)
    elif date_range == "last_year":
        start = today.replace(year=today.year - 1, month=1, day=1)
        end = start.replace(month=12, day=31)
    else:
        raise ValueError("Unsupported date range: {}".format(date_range))

    end = end.replace(hour=23, minute=59)
    return start.strftime(DATE_FORMAT), end.strftime(DATE_FORMAT)


def get_output_names(config, kind):
    names = []
    for bound in ("start", "end"):
        name = config.get(bound + "_" + kind + "_name", bound + "_date")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("{} {} name must not be empty.".format(bound.title(), kind))
        names.append(name.strip())
    if names[0] == names[1]:
        raise ValueError("Start and end {} names must be different.".format(kind))
    return tuple(names)
