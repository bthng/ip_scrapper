import os
import requests
import justext
from datetime import date, timedelta
from subprocess import call
import csv
import pandas as pd

# dt = ( date.today().strftime("%Y_%m_%d") - 1)
WHOIS_USERNAME_DAILY = os.environ['WHOIS_USERNAME_DAILY']
WHOIS_PASSWORD_DAILY = os.environ['WHOIS_PASSWORD_DAILY']

for i in range(1, 2):

    dt = (date.today() - timedelta(days=i)).strftime("%Y_%m_%d")
    print (dt)

    domain='add'

    def dl_files():
        with open('../data/whois_add_total.txt', 'r') as f:
            # rf = f.readlines()
            for line in f:
                folderNm = line.strip()
                if domain == 'add':
                   url = f"http://{WHOIS_USERNAME_DAILY}:{WHOIS_PASSWORD_DAILY}@bestwhois.org/domain_name_data/domain_names_whois/{domain}_{dt}/{folderNm}/"
                else:
                    url = f"http://{WHOIS_USERNAME_DAILY}:{WHOIS_PASSWORD_DAILY}@bestwhois.org/domain_name_data/domain_names_dropped_whois/{domain}_{dt}/{folderNm}/"

                # print (url)
                response = requests.get(url)

                paragraphs = justext.justext(response.content, justext.get_stoplist("English"))
                for paragraph in paragraphs:
                    csvFiles = paragraph.text


                char1 = '/'
                char2 = ' '

                lines = csvFiles.split('\n')
                for line in lines:
                    line1 = line[line.find(char1)+1 : line.find(char2)]
                    # print (line1)
                    newFile = line1

                    if line1 != '':

                        if domain == 'add':
                            dlurl = f"http://{WHOIS_USERNAME_DAILY}:{WHOIS_PASSWORD_DAILY}@bestwhois.org/domain_name_data/domain_names_whois/{domain}_{dt}/{folderNm}/{line1}"
                        else:
                            dlurl = f"http://{WHOIS_USERNAME_DAILY}:{WHOIS_PASSWORD_DAILY}@bestwhois.org/domain_name_data/domain_names_dropped_whois/{domain}_{dt}/{folderNm}/{line1}"


                        res1 = requests.get(dlurl)

                        if f"{domain}_{dt}" not in os.listdir("../results"):
                            os.mkdir(f"../results/{domain}_{dt}")
                        if folderNm not in os.listdir(f"../results/{domain}_{dt}"):
                            os.mkdir(f"../results/{domain}_{dt}/{folderNm}")
                        with open(os.path.join(f"../results/{domain}_{dt}/{folderNm}", newFile), 'wb') as f:
                            f.write(res1.content)

    def merge_files():
        with open('../data/whois_add_total.txt', 'r') as f:
            # rf = f.readlines()
            for line in f:
                folderNm = line.strip()
                if f"{domain}_{dt}" not in os.listdir("../results_merged"):
                    os.mkdir(f"../results_merged/{domain}_{dt}")
                try:
                  script= f"awk '(NR == 1) || (FNR > 1)' ../results/{domain}_{dt}/{folderNm}/*.csv > ../results_merged/{domain}_{dt}/{folderNm}.csv"
                  call(script,shell=True)
                except:
                  print("Error encountered")




    def final_results():
        with open('../data/whois_add_total.txt', 'r') as f:
            for line in f:
                folderNm = line.strip()
                print (f"Running {folderNm}")
                with open(f"../results_merged/{domain}_{dt}/{folderNm}.csv","rb") as source:
                    try:
                        f=pd.read_csv(f"../results_merged/{domain}_{dt}/{folderNm}.csv", low_memory=False)

                        keep_col = ['domainName', 'registrarName', 'contactEmail', 'nameServers', 'createdDate', 'updatedDate', 'expiresDate', 'standardRegCreatedDate', 'standardRegUpdatedDate', 'standardRegExpiresDate']
                        new_f = f[keep_col]
                        if f"{domain}_{dt}" not in os.listdir("../results_final_whoisdaily"):
                            os.mkdir(f"../results_final_whoisdaily/{domain}_{dt}")
                        new_f.to_csv(f"../results_final_whoisdaily/{domain}_{dt}/{folderNm}.csv", index=False)
                    except Exception as e:
                        print("Error encountered")
                        print(e)

    def main():
        dl_files()
        merge_files()
        final_results()


    main()
