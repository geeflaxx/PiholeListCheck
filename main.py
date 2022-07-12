import socket
import os
import requests
from alive_progress import alive_bar
import pyfiglet
import sys
from datetime import datetime
#########################################################
#       Add your list of websites in listofsite.txt     #
#########################################################

## Variables
sites = []  # Websites to have the list of adds
blockAdSites = []   # adwebsites

availableSites = []  # Websites are online
availableAd = []   # Adsites are online

notAvailableSites = []  # Websites are offline
notAvailableAd = [] # Adsites are offline


# anpingen | check available Sites
def checkSites():
    with open("listofsites.txt", "r") as file:
        for hostname in file:
            if len(hostname) < 3:
                continue
            if hostname[-1] == '\n':
                hostname = hostname[:-1]
                #siteIP = socket.gethostbyname(siteIP)
            result = os.popen(f"curl {hostname}").read()

            if result != "":
                availableSites.append(hostname)
            else:
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
            # will scan ports between 1 to 65,535
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






# check ad sites
def checkAdSites():
    for url in availableSites:  # every site
        req = requests.get(url)
        arr = req.text.split('\n')
        with alive_bar() as bar:
            bar.current()
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
        for element in availableAd:
            file.write(element)


#def checkDuplicates():


if __name__ == '__main__':
    ascii_banner = pyfiglet.figlet_format("Ad Checker")
    print(ascii_banner)
    print('-' * 50)
    print(f'Start Scanning: {datetime.now().replace(microsecond=0)}')
    print('-' * 50)
    checkSites()    # to check the website
    checkAdSites()  # to check the Ad-Site
