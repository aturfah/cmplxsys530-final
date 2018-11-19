""" Script to pull in gen7pu data """
import requests
from datetime import datetime, timedelta


def get_url_base(lag=1):
    """
    Get the month to use for the data.

    Args:
        lag (int): Number of months to push back.

    Returns:
        Month <lag> months behind in YYYY-MM format.

    """
    current_time = datetime.today().replace(day=1)
    current_time = current_time - timedelta(months=lag)
    time_str = current_time.strftime("%Y-%m")
    url_base = "http://www.smogon.com/stats/{month}/chaos".format(month=time_str)
    print(requests.get(url_base))
    return url_base


if __name__ == "__main__":
    print("Starting Data Retreival")
    TIERS = ["ou", "uu", "ru", "nu", "pu"]
    BASE_URL = "{url_base}/gen7{tier}-{level}.json".format(url_base=get_url_base())
    LEVELS = [0, 1500, 1630, 1760]
    OU_LEVELS = [0, 1500, 1695, 1825]

    raise RuntimeError("DOOT")

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
