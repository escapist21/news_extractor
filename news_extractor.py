# all imports
import requests
from bs4 import BeautifulSoup
import re
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import pandas as pd
from tqdm import tqdm, tqdm_notebook


class Analysis:

    def __init__(self, term, site, b_date, e_date):
        self.fmt_term = '+'+'+'.join(term.split())
        self.site = site
        self.b_date = b_date
        self.e_date = e_date
        self.url = "https://www.google.com/search?q=allinurl:{}+site:{}&lr=lang_hi&hl=en&as_qdr=all&tbs=lr:lang_1hi,cdr:1,cd_min:{},cd_max:{}".format(
            self.fmt_term, self.site, self.b_date, self.e_date)

    def open_driver(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome()
        driver = self.driver

        return driver

    def close_driver(self):
        self.driver.quit()

    def result_length(self):
        driver = self.open_driver()
        url = self.url
        col_length = None
        driver.get(url)
        try:
            cols = driver.find_elements_by_xpath('//*[@id="xjs"]/div/table/tbody/tr/td')
            col_length = len(cols) - 2
        except NoSuchElementException:
            print('No such element found')
        self.close_driver()
        if col_length is not None:
            return col_length
        else:
            return 0

    def href_extactor(self):
        hrefs = []
        result = 1
        driver = self.open_driver()
        pages = self.result_length()
        print("Search result pages found: {}".format(pages))
        print("Downloading data from search results...")
        old_url = self.url
        # print(old_url)
        if pages <= 0:
            driver.get(old_url)
            sleep(5)
            anchors = driver.find_elements_by_tag_name('a')
            for a in anchors:
                href = a.get_attribute('href')
                if href is not None:
                    hrefs.append(href)
            self.close_driver()
        else:
            for i in range(pages):
                append_str = '&start='+str(result)
                new_url = old_url+append_str
                # print('Downloading from: '+new_url)
                driver.get(new_url)
                sleep(5)
                anchors = driver.find_elements_by_tag_name('a')
                for a in anchors:
                    href = a.get_attribute('href')
                    if href is not None:
                        hrefs.append(href)
                self.close_driver()
                result += 10
        # extracting valid urls from hrefs and storing in a list
        urls = []
        for href in hrefs:
            urls.extend(re.findall('https://www.{}.+'.format(self.site), href))
        # removing duplicate urls
        urls_clean = list(set(urls))

        return urls_clean

    def make_data(self):
        headings = []
        date = []
        urls = self.href_extactor()

        print('Making data file')
        for i in tqdm(range(len(urls)), desc='Progress'):
            r = requests.get(urls[i])
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, 'html.parser')
                try:
                    headings.append(soup.h1.text)
                except AttributeError:
                    headings.append('Does not exist')

                try:
                    date.append(soup.time.text)
                except AttributeError:
                    date.append('Does not exist')

        data = list(zip(headings, date, urls))
        df = pd.DataFrame(data=data, columns=['heading', 'date', 'url'])
        df_name = (str.split(self.site, ',')[0])
        df.to_csv('{}.csv'.format(df_name), index=None)
        return df

