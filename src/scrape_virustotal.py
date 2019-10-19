#!/usr/local/bin/python3
import pandas as pd
from datetime import date
import os
from helpers import scrape_single_vt, scrape_all


def main():
    _date = date.today().strftime("%Y%m%d")
    cols=["ip_address", "negative_count", "positive_count", "discovery_date"]
    ip_list = list(pd.read_csv(f"data/{_date}/ip_list.csv")['ip_addresses'])
    df = scrape_all(ip_list, cols, scrape_single_vt, debug=True)
    if _date not in os.listdir("results"):
        os.mkdir(f"results/{_date}")
    df.to_csv(f"results/{_date}/virustotal.csv", index=False)

    
if __name__ == "__main__":
    main()