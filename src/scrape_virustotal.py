#!/usr/local/bin/python3
import requests
import pandas as pd
from datetime import date
import os

API_KEY = "11c538211c697150a3eab76db784a7a31995bc810c2b78093015ec005614689c"

def scrape_single(ip_address, debug):
    """Scrape for a single ip address
    
    Arguments:
        ip_address {String} -- ip_address

    Returns:
        {dictionary} -- result
    """
    api_url = "https://www.virustotal.com/vtapi/v2/url/report"
    params = {'apikey': API_KEY, 'resource': ip_address}
    response = requests.get(api_url, params=params)

    negative_count = "NA"
    positive_count = "NA"
    discovery_date = "NA"

    if response.status_code == 200 and response.json()['response_code']==1:
        response_json = response.json()
        negative_count = response_json['total'] - response_json['positives']
        positive_count = response_json['positives']
        discovery_date = response_json['scan_date']
        
    
    result = {
        "ip_address": ip_address,
        "negative_count": negative_count,
        "positive_count": positive_count,
        "discovery_date": discovery_date
    }

    if debug:
        print(f"Scraping for {ip_address}: statuscode={response.status_code}")
    return result
        
def scrape_all(ip_list, debug=False):
    """Scrape for a list of ip addresses

    Arguments:
        ip_list {List} -- List of ip addresses

    Returns:
        {Dataframe} -- dataframe with all the results
    """
    cols=["ip_address", "negative_count", "positive_count", "discovery_date"]

    df = pd.concat([pd.DataFrame([scrape_single(ip, debug=debug)], columns=cols) for ip in ip_list],ignore_index=True)
    return df


def main():
    _date = date.today().strftime("%Y%m%d")
    ip_list = list(pd.read_csv(f"data/{_date}/ip_list.csv")['ip_addresses'])
    df = scrape_all(ip_list, debug=True)
    if _date not in os.listdir("results"):
        os.mkdir(f"results/{_date}")
    df.to_csv(f"results/{_date}/virustotal.csv", index=False)

    
if __name__ == "__main__":
    main()