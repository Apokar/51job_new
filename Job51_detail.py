# -*- coding: utf-8 -*-
# @Time         : 2017/11/20 17:04
# @Author       : Huaiz
# @Email        : Apokar@163.com
# @File         : Job51_detail.py
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
    while True:
        try:
            req = requests.get(url, timeout=10, headers=headers, verify=False)
            return req
        except Exception, e:
            print 'get_parse error  : ' + str(e)
            continue


def get_detail_pages(s_date):
    while True:
        try:
            conn = MySQLdb.connect(host="139.198.189.129", port=20009, user="root", passwd="somao1129",
                                   db="51job",
                                   charset="utf8")
            cursor = conn.cursor()

            print s_date

            dateline = str(s_date)
            s_time = dateline[:4] + '-' + dateline[4:6] + '-' + dateline[6:8]
            cursor.execute('select job_url from 51job_single_url where datestamp > "%s"' % (
                s_time
            ))
            need = cursor.fetchall()
            need_urls = []
            for y in range(0, len(need)):
                need_urls.append(need[y][0])

            # cursor.execute('select distinct a.job_url from 51job_career_list_copy a left join 51job_career_detail_all b on a.job_url = b.job_url where b.job_url is null')
            # need = cursor.fetchall()
            #
            # for y in range(0, len(need)):
            #     need_urls.append(need[y][0])
            return need_urls
            break
        except Exception,e:
            if str(e).find('2013')>=0:
                print '2013 error , reconnect '+ str(datetime.datetime.now())
                cursor.close()
                conn.close()

                conn = MySQLdb.connect(host="139.198.189.129", port=20009, user="root", passwd="somao1129",db="51job",charset="utf8")
                cursor = conn.cursor()
                continue
            elif str(e).find('2013')>=0:
                print '2016 error , reconnect '+ str(datetime.datetime.now())
                cursor.close()
                conn.close()
                conn = MySQLdb.connect(host="139.198.189.129", port=20009, user="root", passwd="somao1129",db="51job",charset="utf8")
                cursor = conn.cursor()
                continue
            else:
                print str(e) + str(datetime.datetime.now())
                break


def get_info(url):
    print 'getting 2nd page : ' + url + ' _@_ ' + str(datetime.datetime.now())

    req = get_parse(url)
    content = str(req.text).encode('latin1').decode('gbk')
    print type(content)
    conn = MySQLdb.connect(host="139.198.189.129", port=20009, user="root", passwd="somao1129",
                           db="51job",
                           charset="utf8")
    cursor = conn.cursor()
    try:
        info = re_findall('class="msg ltype">(.*?)</p>', content)
        job_name = re_findall('<h1 title=".*?">(.*?)<input value', content)[0]
        company_url = re.findall('<a href="(.*?)" target="_blank" title=".*?">.*?<em class="icon_b i_link">', content)[
            0]
        company_name = re.findall('<a href=".*?" target="_blank" title="(.*?)">.*?<em class="icon_b i_link">', content)[
            0]
        salary = re_findall('<strong>(.*?)</strong>', content)[1]

        location = re_findall('<span class="lname">(.*?)</span>', content)[0]
        pub_date = re.findall('<em class="i4"></em>(.*?)</span>', content)[0]

        expr = re_findall('class="i1"></em>(.*?)</span>', content)[0]
        edu = re_findall('class="i2"></em>(.*?)</span>', content)[0]
        hire_number = re_findall('class="i3"></em>(.*?)</span>', content)[0]
        label = re_findall('class="t2">.*?<span>(.*?)</p>', content)[0]
        job_des = re_findall('class="bmsg job_msg inbox">(.*?)<div class="mt10">', content)[0]
        career_type = re_findall('<span class="el">(.*?)</span>', content)[0]
        address = re_findall('<span class="label">上班地址：</span>(.*?)</p>', str(content))[0]
        company_des = re_findall('class="tmsg inbox">(.*?)</div>', content)[0]

        print url
        print job_name
        print company_url
        print company_name
        print salary
        print location
        print pub_date[:-2]
####
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
        cursor.execute(
            'insert into 51job_career_detail_all values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
            (
                url
                ,job_name
                ,company_url
                ,company_name
                ,salary
                ,location
                ,pub_date[:-2]
                , isExist(detag(info[0]).split('|')[0])
                , isExist(detag(info[0]).split('|')[1])
                , isExist(detag(info[0]).split('|')[2])
                , detag(expr)
                , detag(edu)
                , hire_number
                , detag(label.replace('</span>', '').replace('<span>', '|'))
                , detag(job_des)
                , career_type
                , detag(address)
                , detag(address)
                , detag(company_des)
                , str(datetime.datetime.now())
                , str(datetime.datetime.now())[:10]
            )
        )
        conn.commit()
        print u'详情页 插入成功 @' + str(datetime.datetime.now())

    except Exception, e:
        if str(e).find('2006') >= 0:
            cursor.close()
            conn.close()
            conn = MySQLdb.connect(host="139.198.189.129", port=20009, user="root", passwd="somao1129",
                                   db="51job", charset="utf8")
            cursor = conn.cursor()
            print '数据库连接重启  ' + str(datetime.datetime.now())


        elif str(e).find('10064') >= 0:
            print url + ' --插入数据错误  ' + str(datetime.datetime.now())
            cursor.execute('insert into 51job_error_log values("%s","%s","%s","%s")' % (
                url, '10064', '2nd_page', str(datetime.datetime.now())))
            conn.commit()
            print '错误信息 录入日志表 51job_error_log  ' + str(datetime.datetime.now())
        else:
            print str(e)
            print url + '出错,跳过  ' + str(datetime.datetime.now())
            cursor.execute('insert into 51job_error_log values("%s","%s","%s","%s")' % (
                url, 'unknown', '2nd_page', str(datetime.datetime.now())))
            conn.commit()


def main():
    need_urls = get_detail_pages()
    for url in need_urls:
        get_info(url)
