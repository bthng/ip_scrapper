import requests
import pandas as pd
from datetime import date
import os
from helpers import scrape_single_asn, scrape_all



def main():
    _date = date.today().strftime("%Y%m%d")
    cols=["ip_address", "ip_range", "as_number", "provider_name"]
    ip_list = list(pd.read_csv(f"data/{_date}/ip_list.csv")['ip_addresses'])
    df = scrape_all(ip_list, cols, scrape_single_asn, debug=True)
    if _date not in os.listdir("results"):
        os.mkdir(f"results/{_date}")
    df.to_csv(f"results/{_date}/asn.csv", index=False)

    
if __name__ == "__main__":
    main()