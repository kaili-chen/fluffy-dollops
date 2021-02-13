import sys
import requests
from bs4 import BeautifulSoup

# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
url = ""
webpage = requests.get(url)
if webpage.status_code != 200:
    sys.exit("status code {}, exiting script".format(webpage.status_code))

soup = BeautifulSoup(webpage.text, "html.parser")
if soup is None or soup == "":
    sys.exit("soup empty, exiting script")

# find by div with class name "test"
divs = soup.find_all("div", {"class": "test"})
