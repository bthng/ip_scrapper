
## IP Scrapper
Scripts used to scrape IP results for TW.

- Step1: Create a new `.env` file, copy and paste template from `.env_demo` over
- Step2: `source .env`


### asn
to run: `python3 src/crawl_asn.py` | will crawl for current day
output: asn_results folder

### virustotal
to run: `python3 src/virustotal.py` | will crawl for current day
output: virustotal_results folder

https://developers.virustotal.com/reference#ip-address-report

### whois quarterly
to run: `python3 ccTLDs.py`
to run: `python3 gTLDs.py`
output: cctlds and gtlds folder respectively

### whois daily
to run: `python3 whois_daily.py` | will crawl for current day
output: results_final_whoisdaily folder
