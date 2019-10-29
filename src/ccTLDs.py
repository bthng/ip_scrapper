from TLDS_Lib import getting_path, download_unzip_file

def main():
    url = 'http://domainwhoisdatabase.com/domain_list_quarterly/v15/csv/tlds/simple/'
    username = 'Whois_Last_QDB_Trial_10_2019'
    password = 'eb3wFRWFXbaD'
    url_info = [url,username,password]
    folder_name = __file__.split(".")[0]

    all_file_names = getting_path(url_info)

    for file in all_file_names[]:
        download_unzip_file(url_info,file,folder_name)

if __name__ == "__main__":
    main()
