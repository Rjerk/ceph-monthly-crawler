#!/usr/local/bin/python3

import datetime
import time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as expected
# from selenium.webdriver.support.wait import WebDriverWait

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=chrome_options)

def get_html(url):
    try:
        driver.get(url)
        # wait.until(expected.visibility_of_element_located((By.NAME, 'q'))).send_keys('headless firefox' + Keys.ENTER)
        # wait.until(expected.visibility_of_element_located((By.CSS_SELECTOR, '#ires a'))).click()
    except:
        print ("Have a problem when get: {}".format(url), file=weird)
    time.sleep(2)
    return driver.page_source

def this_month():
    return datetime.datetime.now().month

soup = BeautifulSoup(get_html('https://github.com/ceph/ceph/pulse/monthly'), 'html.parser')

less  = open('less',  'w')
more  = open('more',  'w')
weird = open('weird', 'w')

for li in soup.find_all('li'):
    if li.span and li.span.string and 'Merged' in li.span.string:
        pr_merged_time = li.find('relative-time').get('datetime')
        t = datetime.datetime.strptime(pr_merged_time, '%Y-%m-%dT%H:%M:%SZ')

        if t.month == this_month():
            pr_id = li.find_all('span', 'num')[0].string
            pr_title = li.a.string
            pr_link = 'https://github.com' + li.a.get('href')
            print ("Hi, {}".format(pr_link))

            new_soup = BeautifulSoup(get_html(pr_link), 'html.parser')
            diff_stat = new_soup.find(id='diffstat')

            if not diff_stat:
                print ("Weird, no diff_stat ?", file=weird)
                print ('[', pr_id, t.date(), ']', file=weird)
                print (pr_title, '\n', pr_link, '\n', file=weird)
                print (file=weird)
                print (file=weird)
                continue

            incre = diff_stat.contents[1].string.strip().strip('+').replace(',', '')
            decre = diff_stat.contents[3].string.strip().strip('−').replace(',', '')
            if 0 <= int(incre) <= 10 and 0 <= int(decre) <= 10:
                print ('[', pr_id, t.date(), ']', file=less)
                print (pr_title, '==> +{}'.format(incre), '-{}'.format(decre), \
                       '\n', pr_link, '\n', file=less)
            else:
                print ('[', pr_id, t.date(), ']', file=more)
                print (pr_title, '==> +{}'.format(incre), '-{}'.format(decre), \
                       '\n', pr_link, '\n', file=more)

driver.quit()
