""" Script to pull in gen7pu data """
import requests


if __name__ == "__main__":
    print("Starting Data Retreival")
    TIERS = ["ou", "uu", "ru", "nu", "pu"]
    BASE_URL = "http://www.smogon.com/stats/2017-12/chaos/gen7{tier}-{level}.json"
    LEVELS = [0, 1500, 1630, 1760]

    for tier in TIERS:
        for level in LEVELS:
            print("\t{}-{}".format(tier, level))
            raw_html = requests.get(BASE_URL.format(tier=tier, level=level)).content
            file_ = open("raw_data/gen7{tier}-{level}.json".format(tier=tier,
                                                                   level=level), mode='wb')
            file_.write(raw_html)
            file_.close()

    print("Completed")
