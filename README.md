
## IP Scrapper
Scripts used †o scrape IP results for TW.

- Step1: Create a new `.env` file, copy and paste template from `.env_demo` over
- Step2: `source .env`


### asn
to run: `python3 src/crawl_asn.py`
output: asn_results folder

### virustotal
to run: `python3 src/virustotal.py`
output: virustotal_results folder
https://developers.virustotal.com/reference#ip-address-report

### whois quarterly
to run: `python3 ccTLDs.py`
to run: `gTLDs.py`
output: cctlds and gtlds folder respectively

### whois daily
to run: `python3 whois_daily.py`
output: results_final_whoisdaily folder
