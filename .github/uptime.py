"""Update the Uptime line in dark_mode.svg and light_mode.svg.

GitHub Actions runs this every hour (see workflows/uptime.yml).
"""
import datetime as dt
import re
from pathlib import Path
from zoneinfo import ZoneInfo

BIRTH_TZ = ZoneInfo("Asia/Shanghai")  # China time, where the birth time was recorded
BIRTH = dt.datetime(1998, 3, 22, 17, 40, tzinfo=BIRTH_TZ)
WIDTH_CHARS = 58  # must match the card generator
ROOT = Path(__file__).resolve().parent.parent

PATTERN = re.compile(
    r'(<tspan class="cc" id="uptime_dots">)[^<]*'
    r'(</tspan><tspan class="value" id="uptime_data">)[^<]*(</tspan>)')


def plural(n, word):
    return f"{n} {word}{'' if n == 1 else 's'}"


def uptime(now):
    now = now.astimezone(BIRTH_TZ)
    years = now.year - BIRTH.year
    months = now.month - BIRTH.month
    days = now.day - BIRTH.day
    minutes = (now.hour * 60 + now.minute) - (BIRTH.hour * 60 + BIRTH.minute)
    if minutes < 0:
        days -= 1
        minutes += 24 * 60
    if days < 0:
        months -= 1
        last_month_end = now.date().replace(day=1) - dt.timedelta(days=1)
        days += last_month_end.day
    if months < 0:
        years -= 1
        months += 12
    return (f"{plural(years, 'year')}, {plural(months, 'month')}, "
            f"{plural(days, 'day')}, {plural(minutes // 60, 'hour')}")


def main():
    value = uptime(dt.datetime.now(dt.timezone.utc))
    dots = "." * (WIDTH_CHARS - len(". Uptime: ") - len(value) - 1)
    for name in ("dark_mode.svg", "light_mode.svg"):
        path = ROOT / name
        svg = path.read_text(encoding="utf-8")
        new = PATTERN.sub(lambda m: f"{m[1]} {dots} {m[2]}{value}{m[3]}", svg)
        if new != svg:
            path.write_text(new, encoding="utf-8")
    print("Uptime:", value)


if __name__ == "__main__":
    main()
