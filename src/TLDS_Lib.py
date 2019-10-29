import os
import requests
import gzip
import pandas as pd
from bs4 import BeautifulSoup

def getting_path(url_info):
    r = requests.get(url_info[0], auth=(url_info[1], url_info[2]))

    if r:
        print('Success!')
    else:
        print('An error has occurred.')

    html = r.content
    soup = BeautifulSoup(html,'lxml')
    all_files = [file.get('href') for file in soup.find_all("a") if file.get('href').endswith('.gz')]
    print("All file names are retrieved!")

    return all_files

def download_unzip_file(url_info,file_name,folderName):
    file_url = url_info[0] + file_name
    print(file_url)
    folder_name = './' + folderName + '/'

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"{folder_name} folder is created.")

    r = requests.get(file_url, auth=(url_info[1], url_info[2]))

    with open(os.path.join(folder_name, file_name), 'wb') as f:
        f.write(r.content)

    if (os.path.getsize(f'{folder_name}{file_name}')/(1024 * 1024 * 1024)) < 2:
        with gzip.open(f'{folder_name}{file_name}','rb') as f:
            pd.read_csv(f,low_memory=False).to_csv(f"{folder_name}{'_'.join(file_name.split('.')[1:-3])}.csv",index=False)

        if os.path.exists(f"{folder_name}{file_name}"):
            os.remove(f"{folder_name}{file_name}")
        else:
            print("The file does not exist")
    else:
        print(f"{file_name} is more than 2G. Unzip process is passed!")
