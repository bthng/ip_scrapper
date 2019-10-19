import requests
import pandas as pd
from datetime import date
import os

def scrape_single(ip_address, debug):
    """Scrape for a single ip address
    
    Arguments:
        ip_address {String} -- ip_address

    Returns:
        {dictionary} -- result
    """
    api_url = f"https://api.iptoasn.com/v1/as/ip/{ip_address}"
    response = requests.get(api_url)

    as_number = "NA"
    ip_range = "NA"
    provider_name = "NA"
    if response.status_code == 200 and response.json()['announced']:
        response_json = response.json()
        as_number = response_json['as_number']
        ip_range = [response_json['first_ip'], response_json['last_ip']]
        provider_name = response_json['as_description']
    
    result = {
        "ip_address": ip_address,
        "ip_range": ip_range,
        "as_number": as_number,
        "provider_name": provider_name
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
    cols=["ip_address", "ip_range", "as_number", "provider_name"]

    df = pd.concat([pd.DataFrame([scrape_single(ip, debug=debug)], columns=cols) for ip in ip_list],ignore_index=True)
    return df


def main():
    _date = date.today().strftime("%Y%m%d")
    ip_list = list(pd.read_csv(f"data/{_date}/ip_list.csv")['ip_addresses'])
    df = scrape_all(ip_list, debug=True)
    if _date not in os.listdir("results"):
        os.mkdir(f"results/{_date}")
    df.to_csv(f"results/{_date}/asn.csv", index=False)

    
if __name__ == "__main__":
    main()