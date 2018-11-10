import requests
import re
from bs4 import BeautifulSoup


class BaseGenerator(object):

    def __init__(self):
        pass

    @staticmethod
    def get_soup(link):
        while True:
            for i in range(20):
                try:
                    html_page = requests.get(link, timeout=15).text
                except requests.exceptions.RequestException:
                    print("Could not open {}. Retrying...".format(link))
                else:
                    return BeautifulSoup(html_page, "lxml")
            try:
                requests.get("https://www.google.com", timeout=10)
                raise Exception("Internet works, but could not connect")
            except requests.ConnectionError:
                print("Problem with internet connection")

    def _id_generators(self, ids, pattern, base_url, offset_step):
        if not isinstance(ids, tuple):
            ids = ([ids])

        offset = 0
        url = base_url.format(*ids, offset)
        while True:
            soup = self.get_soup(url)
            set_of_ids = soup.find_all("a", href=re.compile(pattern))
            set_of_ids = [a.get("href") for a in set_of_ids if a]
            set_of_ids = [
                re.search(pattern, a) for a in set_of_ids]
            set_of_ids = {a.group(1) for a in set_of_ids if a}

            if not set_of_ids:
                return

            for h in set_of_ids:
                yield h

            offset += offset_step
            url = base_url.format(*ids, offset)
            if not soup.find("a", attrs={"data-offset": offset}):
                return
