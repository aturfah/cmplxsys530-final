"""Script to pull in PS usage data."""
import os
from datetime import datetime

import requests


def prepare_folders():
    """Create folders to store usage data (if not already present)."""
    if not os.path.exists("data/usage"):
        os.makedirs("data/usage")


def monthdelta(delta):
    """
    Get the day <delta> months back.

    Args:
        date (datetime): Datetime to be calculated from.
        delta (int): Amount to change month by.

    Returns:
        datetime object <delta> months back

    """
    date = datetime.today()
    month, year = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not month:
        month = 12
    day = min(date.day, [31,
                         29 if year % 4 == 0 and not year % 400 == 0 else 28,
                         31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month-1])
    return date.replace(day=day, month=month, year=year)


def get_url_base(lag=-1):
    """
    Get the month to use for the data.

    Args:
        lag (int): Number of months to push back.

    Returns:
        Month <lag> months behind in YYYY-MM format.

    """
    current_time = monthdelta(lag)
    time_str = current_time.strftime("%Y-%m")
    url_base = "http://www.smogon.com/stats/{month}/chaos".format(month=time_str)

    # Verify that we have data for the previous month
    if requests.get(url_base).status_code != 200:
        return get_url_base(lag=lag-1)

    return url_base


if __name__ == "__main__":
    print("Starting Data Retreival")
    TIERS = ["ou", "uu", "ru", "nu", "pu"]
    BASE_URL = "{url_base}/gen7{tier}-{level}.json".replace("{url_base}", get_url_base())
    LEVELS = [0, 1500, 1630, 1760]
    OU_LEVELS = [0, 1500, 1695, 1825]

    prepare_folders()
    for tier in TIERS:
        for ind, level in enumerate(LEVELS):
            if tier == "ou":
                level = OU_LEVELS[ind]

            print("\tFetching {}-{}".format(tier, level))
            raw_html = requests.get(BASE_URL.format(tier=tier, level=level)).content
            file_ = open("data/usage/gen7{tier}-{level}.json".format(tier=tier,
                                                                     level=level), mode='wb')
            file_.write(raw_html)
            file_.close()

    print("Completed")
