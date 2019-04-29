#!/usr/local/bin/python3

import datetime

import requests
from bs4 import BeautifulSoup

r = requests.get('https://github.com/ceph/ceph/pulse/monthly')

html_text = r.text

soup = BeautifulSoup(html_text, 'html.parser')

less = open('less', 'a')
more = open('more', 'a')
weird = open('weird', 'a')

for li in soup.find_all('li'):
    if li.span and li.span.string and 'Merged' in li.span.string:
        pr_merged_time = li.find('relative-time').get('datetime')
        t = datetime.datetime.strptime(pr_merged_time, '%Y-%m-%dT%H:%M:%SZ')
        if t.month == datetime.datetime.now().month:
            pr_id = li.find_all('span', 'num')[0].string
            pr_title = li.a.string
            pr_link = 'https://github.com' + li.a.get('href')
            new_soup = BeautifulSoup(requests.get(pr_link).text, 'html.parser')
            diff_stat = new_soup.find(id='diffstat')
            if not diff_stat:
                print ("Weird, no diff_stat ?", file=weird)
                print (file=weird)
                print (file=weird)
                print ('[', pr_id, t.date(), ']', file=werid)
                print (pr_title, '\n', pr_link, '\n', file=weird)
                continue

            incre = diff_stat.contents[1].string.strip().strip('+').replace(',', '')
            decre = diff_stat.contents[3].string.strip().strip('−').replace(',', '')
            if 0 <= int(incre) <= 10 and 0 <= int(decre) <= 10:
                print ('[', pr_id, t.date(), ']', file=more)
                print (pr_title, '==> +{}'.format(incre), '-{}'.format(decre), '\n', pr_link, '\n', file=less)
            else:
                print ('[', pr_id, t.date(), ']', file=more)
                print (pr_title, '==> +{}'.format(incre), '-{}'.format(decre), '\n', pr_link, '\n', file=more)
