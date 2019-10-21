import requests
import pandas as pd

VT_API_KEY = "11c538211c697150a3eab76db784a7a31995bc810c2b78093015ec005614689c"

def scrape_single_asn(ip_address, debug):
    """Scrape for a single ip address
    
    Arguments:
        ip_address {String} -- ip_address

    Returns:
        {dictionary} -- result
    """
    api_url = f"https://api.iptoasn.com/v1/as/ip/{ip_address}"
    response = requests.get(api_url)

    as_number = "NA"
    provider_name = "NA"
    ip_range_start = "NA"
    ip_range_last = "NA"
    if response.status_code == 200 and response.json()['announced']:
        response_json = response.json()
        as_number = response_json['as_number']
        ip_range_start = response_json['first_ip']
        ip_range_last = response_json['last_ip']
        provider_name = response_json['as_description']
    
    result = {
        "ip_address": ip_address,
        "ip_range_start": ip_range_start,
        "ip_range_last": ip_range_last,
        "as_number": as_number,
        "provider_name": provider_name
    }
    if debug:
        print(f"Scraping for {ip_address}: statuscode={response.status_code}")
    return result
    

def scrape_single_vt(ip_address, debug):
    """Scrape for a single ip address
    
    Arguments:
        ip_address {String} -- ip_address

    Returns:
        {dictionary} -- result
    """
    api_url = "https://www.virustotal.com/vtapi/v2/url/report"
    params = {'apikey': VT_API_KEY, 'resource': ip_address}
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


def scrape_all(ip_list, cols, scrape_single, debug=False):
    """Scrape for a list of ip addresses

    Arguments:
        ip_list {List} -- List of ip addresses

    Returns:
        {Dataframe} -- dataframe with all the results
    """
    df = pd.concat([pd.DataFrame([scrape_single(ip, debug=debug)], columns=cols) for ip in ip_list],ignore_index=True)
    return df