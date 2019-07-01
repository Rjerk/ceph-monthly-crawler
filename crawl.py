#!/usr/local/bin/python3

import datetime
import time

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import xlsxwriter

wb = xlsxwriter.Workbook("ceph-monthly.xlsx")
ws = wb.add_worksheet(datetime.datetime.now().strftime("%B"))
row = 0

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=chrome_options)

def get_html(url):
    try:
        driver.get(url)
    except:
        print ("Have a problem when get: {}".format(url), file=weird)
    time.sleep(2)
    return driver.page_source

def this_month(month):
    return month == datetime.datetime.now().month

def get_soup(uri):
    return BeautifulSoup(get_html(uri), 'html.parser')

def write_file(row, pr_id, pr_title, pr_link, pr_merged_time, incre, decre):
    ws.write(row, 0, pr_id)
    ws.write(row, 1, pr_title)
    ws.write(row, 2, pr_link)
    ws.write(row, 3, pr_merged_time)
    ws.write(row, 4, incre)
    ws.write(row, 5, decre)

for li in get_soup('https://github.com/ceph/ceph/pulse/monthly').find_all('li'):
    if li.span and li.span.string and 'Merged' in li.span.string:
        pr_merged_time = datetime.datetime.strptime(
                            li.find('relative-time').get('datetime'),
                            '%Y-%m-%dT%H:%M:%SZ'
                         )

        if this_month(pr_merged_time.month):

            pr_id    =  (li.find_all('span', 'num')[0].string)[1:]
            pr_title =  li.a.string
            pr_link  =  'https://github.com' + li.a.get('href')

            print ("{} {} {} {} {}".format(pr_id, pr_title, pr_link, pr_merged_time.date(), pr_merged_time.month))

            diff_stat = get_soup(pr_link).find(id='diffstat')

            if not diff_stat:
                write_weird(row, pr_id, pr_title, pr_link, pr_merged_time.date(), None, None)
                row += 1
                continue

            incre = diff_stat.contents[1].string.strip().strip('+').replace(',', '')
            decre = diff_stat.contents[3].string.strip().strip('−').replace(',', '')

            write_file(row, pr_id, pr_title, pr_link, pr_merged_time.date(), incre, decre)
            row += 1
            #break

driver.quit()
wb.close()
