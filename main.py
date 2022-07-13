import socket # port scan
import os # curl
import requests
from alive_progress import alive_bar # check status
import pyfiglet # looking fine
import sys
from datetime import datetime # date


import time
#########################################################
#       Add your list of websites in listofsite.txt     #
#########################################################

## Variables
sites = []  # Websites to have the list of adds
blockAdSites = []   # adwebsites

availableSites = []  # Websites are online
notAvailableSites = []  # Websites are offline

availableAd = []   # Adsites are online
notAvailableAd = [] # Adsites are offline


# anpingen | check available Sites
def checkSites():
    with open("listofsites.txt", "r") as file:
        with alive_bar(3) as bar:
            for hostname in file:
                bar()
                time.sleep(1)

                if len(hostname) < 3:
                    continue

                hostname = hostname.strip()

                statusOfList = os.popen(f"curl -s {hostname}").read() # Online?

                if statusOfList != "":
                    print("test22")
                    availableSites.append(hostname)
                else:
                    print("TEST")
                    notAvailableSites.append(hostname)



''''
1. erste zeile ( auskommentiert )
2. 0.0.0.0 Seite
3. seite # komment
'''


try:
    with open("list.txt", "r") as file:
        for url in file:
            target = url

            httpPort = 80
            httpsPort = 443
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)

            # returns an error indicator
            result = s.connect_ex((target, httpPort))
            result2 = s.connect_ex((target, httpsPort))
            if result == 0:
                print(f"Port {httpPort} is open")
            if result2 == 0:
                print(f"Port {httpsPort} is open")
            s.close()
except KeyboardInterrupt:
        print("\n Exit")
        sys.exit()
except socket.gaierror:
        print("\n Hostname Could Not Be Resolved !!!!")
except socket.error:
        print("\ Server not responding !!!!")






## check Ad sites
def checkAdSites():
    print(f"Av: {availableSites}")

    for url in availableSites:
        req = requests.get(url)
        arr = req.text.split('\n')
        with alive_bar(len(availableSites)) as bar:
            bar()
            for line in arr:
                    if len(line) < 3 or line[0] == '#':
                        continue
                    if "0.0.0.0" in line:
                        line = line.replace("0.0.0.0", "")
                    if "127.0.0.1" in line:
                        line = line.replace("127.0.0.1", "")
                    if " " in line:
                        line = line.replace(" ", "")
                    if "\n" in line:
                        line = line.replace("\n", "")
                    try:
                        socket.gethostbyname(line)  # Online
                        if line != "":
                            availableAd.append(line)
                    except:
                        notAvailableSites.append(line)  # Offline
            writeAdSiteinFile()

def writeAdSiteinFile():
    with open("availableAd.txt", "w") as file:
        print(f"AD:{availableAd}")
        for element in availableAd:
            file.write(element)


#def checkDuplicates():


if __name__ == '__main__':
    ascii_banner = pyfiglet.figlet_format("PiholeListCheck")
    print(ascii_banner)
    print('-' * 50)
    print(f'Start Scanning: {datetime.now().replace(microsecond=0)}')
    print('-' * 50)
    checkSites()    # to check the website
    checkAdSites()  # to check the Ad-Site
