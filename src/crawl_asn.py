#!/usr/local/bin/python3
import pandas as pd
import requests
from datetime import date
import os

_date = date.today().strftime("%Y%m%d")
ZIPSAVETO = f"/Users/brendathng/Documents/Github/ip_scrapper/tmp/{_date}/asn.tsv.gz"
SAVETO = f"/Users/brendathng/Documents/Github/ip_scrapper/results/{_date}/asn.csv"

def prepare_folders():
    if _date not in os.listdir("/Users/brendathng/Documents/Github/ip_scrapper/results"):
        os.mkdir(f"/Users/brendathng/Documents/Github/ip_scrapper/tmp/{_date}")
        os.mkdir(f"/Users/brendathng/Documents/Github/ip_scrapper/results/{_date}")


def download_file(zipsaveto):
    url="https://iptoasn.com/data/ip2asn-v4-u32.tsv.gz"
    r = requests.get(url)
    with open(zipsaveto, 'wb') as f:
        f.write(r.content)


def clean_data(zipsaveto, saveto):
    df=pd.read_csv(zipsaveto, sep='\t', header=None, compression='gzip')
    df.columns=["range_start", "range_end", "AS_number", "country", "AS_description"]
    df2 = df[["range_start","range_end","AS_number","AS_description"]]
    df2.to_csv(saveto, index=False)


def main():
    prepare_folders()
    download_file(ZIPSAVETO)
    clean_data(ZIPSAVETO, SAVETO)

if __name__ == "__main__":
    main()
