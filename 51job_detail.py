# -*- coding: utf-8 -*-
# @Time         : 2017/11/20 17:04
# @Author       : Huaiz
# @Email        : Apokar@163.com
# @File         : 51job_detail.py
# @Software     : PyCharm Community Edition
# @PROJECT_NAME : 51job_new

import random
import re
import time
import urllib
import datetime
import MySQLdb
import requests
from bs4 import BeautifulSoup

import sys

reload(sys)
sys.setdefaultencoding('utf8')

import urllib3

urllib3.disable_warnings()


def re_findall(pattern, html):
    if re.findall(pattern, html, re.S):
        return re.findall(pattern, html, re.S)
    else:
        return 'N'


def isExist(object_item):
    if object_item:
        return object_item
    else:
        return 'Null'


def detag(html):
    detag = re.subn('<[^>]*>', ' ', html)[0]
    detag = detag.replace('&nbsp;', ' ')
    detag = detag.replace('&ensp;', ';')
    detag = detag.replace(' ', '')
    detag = detag.replace('\t', '')
    detag = detag.replace('\n', '')
    detag = detag.replace('\r', '')
    detag = detag.replace('"', '“')
    detag = detag.replace('\\', '')
    return detag


headers = {
    'User-agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36' \
    , 'Accept-Language': 'zh-CN,zh;q=0.8' \
    , 'Accept-Encoding': 'gzip, deflate, sdch' \
    , 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' \
    , 'Cache-Control': 'max-age=0' \
    , 'Referer': 'http://biz.163.com/' \
    , 'Connection': 'keep-alive' \
    , 'Content-Type': 'application/x-www-form-urlencoded; charset=gbk' \
    , 'Upgrade-Insecure-Requests': '1' \
    }


def get_parse(url):
    # while True:
    #     try:
    req = requests.get(url, timeout=10, headers=headers, verify=False)
    return req
    # except Exception, e:
    #     print 'get_parse error  : ' + str(e)
    #     continue


def get_detail_urls():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="job", charset="utf8")
    cursor = conn.cursor()
    old_urls = []
    all_urls = []
    need_urls = []
    cursor.execute('select job_url from 51job_career_list')
    all = cursor.fetchall()
    for x in range(0, len(all)):
        all_urls.append(all[x][0])

    cursor.execute('select job_url from 51job_career_detail')
    old = cursor.fetchall()
    for y in range(0, len(old)):
        old_urls.append(old[y][0])

    for url in all_urls:
        if url not in old_urls:
            need_urls.append(url)

    return need_urls


def get_info(url):
    print 'getting 2nd page  ' + url + '   ' + str(datetime.datetime.now())

    req = get_parse(url)
    content = str(req.text).encode('latin1').decode('gbk')
    print type(content)
    # try:
    info = re_findall('class="msg ltype">(.*?)</p>', content)
    expr = re_findall('class="i1"></em>(.*?)</span>', content)[0]
    edu = re_findall('class="i2"></em>(.*?)</span>', content)[0]
    hire_number = re_findall('class="i3"></em>(.*?)</span>', content)[0]
    label = re_findall('class="t2">.*?<span>(.*?)</p>', content)[0]
    job_des = re_findall('class="bmsg job_msg inbox">.*?<span class="label">(.*?)<div class="mt10">', content)[0]
    career_type = re_findall('<span class="el">(.*?)</span>', content)[0]
    address = re_findall('<span class="label">上班地址：</span>(.*?)</p>', str(content))[0]
    company_des = re_findall('class="tmsg inbox">(.*?)</div>', content)[0]

    print url
    print isExist(detag(info[0]).split('|')[0])
    print isExist(detag(info[0]).split('|')[1])
    print isExist(detag(info[0]).split('|')[2])
    print detag(expr)
    print detag(edu)
    print hire_number
    print detag(label.replace('</span>', '').replace('<span>', '|'))
    print detag(job_des)
    print career_type
    print detag(address)
    print detag(address)
    print detag(company_des)

    # except Exception:
    #     print '该职位信息现已不存在导致的错误'


url = 'http://jobs.51job.com/changchun/67600199.html?s=01&amp;t=0'
get_info(url)



# urllll = get_detail_urls()
# print urllll[0]
