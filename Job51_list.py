# -*- coding: utf-8 -*-
# @Time         : 2017/11/20 11:06
# @Author       : Huaiz
# @Email        : Apokar@163.com
# @File         : Job51_list.py
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


def get_timestamp(normal_time):
    timeArray = time.strptime(str(normal_time), "%Y%m%d")
    timestamp = time.mktime(timeArray)
    return timestamp


def get_parse(url):
    while True:
        try:
            req = requests.get(url, timeout=10, verify=False)
            return req
        except Exception, e:
            print 'get_parse error  : ' + str(e)
            continue


def get_main_urls():
    main_urls = []
    for b in range(1, 6):
        for c in range(1, 7):
            for d in range(1, 8):
                for a in range(1, 13):
                    if a < 10:
                        main_urls.append('http://search.51job.com/list/000000,000000,0000,00,9,' + '0' + str(
                            a) + ',%2B,2,1.html?lang=c&stype=1&postchannel=0000&workyear=' + '0' + str(
                            b) + '&cotype=99&degreefrom=' + '0' + str(
                            c) + '&jobterm=99&companysize=' + '0' + str(
                            d) + '&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=')

                    else:
                        main_urls.append('http://search.51job.com/list/000000,000000,0000,00,9,' + str(
                            a) + ',%2B,2,1.html?lang=c&stype=1&postchannel=0000&workyear=' + '0' + str(
                            b) + '&cotype=99&degreefrom=' + '0' + str(
                            c) + '&jobterm=99&companysize=' + '0' + str(
                            d) + '&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=')
    print u'获取main_urls  结束:  ' + str(datetime.datetime.now())

    return main_urls


def get_detail_urls(url):
    every_main_urls = []
    while True:
        try:
            req = get_parse(url)
            soup = BeautifulSoup(req.text, 'lxml')
            page_no = soup.select('.og_but')[1]
            num = re.findall('.*?onclick="jumpPage\(\'(.*?)\'\)', str(page_no))
            print u'获取  ' + url + u'的页数' + str(datetime.datetime.now())
            print u'页数为  ' + num[0]
            if num[0] == 1:
                every_main_urls.append(url)
            else:
                for i in range(1, int(num[0]) + 1):
                    every_main_urls.append(
                        url.split('.html')[0][:-1] + str(i) + '.html' + url.split('.html')[1])

            break
        except Exception, e:

            print u'获取列表页: ' + url + u' | 页数部分出错 : ' + str(e)
            break
    return every_main_urls


def get_data(detail_main_url, s_date):
    while True :
        try:
            print 'getting page_info : ' + detail_main_url
            req = get_parse(detail_main_url)
            soup = BeautifulSoup(req.text, 'lxml')
            content = soup.select('div .el')
            conn = MySQLdb.connect(host="139.198.189.129", port=20009, user="root", passwd="somao1129",
                                   db="51job",
                                   charset="utf8")
            cursor = conn.cursor()
            flag = 1
            i = 13
            while flag and (i<len(content)):
                while True:
                    try:

                        print u'获取列表中的信息 ' + str(datetime.datetime.now())

                        html = content[i].encode('latin1').decode('gbk')

                        job_url = re_findall('class="t1 .*?">.*?<a href="(.*?)"', html)[0]
                        # job_name = re_findall('.*?target="_blank" title="(.*?)">', html)[0]
                        # company_url = re_findall('.*?class="t2"><a href="(.*?)"', html)[0]
                        # company_name = re_findall('<span class="t2".*?target="_blank" title="(.*?)"', html)[0]
                        # salary = re_findall('.*?class="t3">(.*?)</span>', html)[0]
                        # lcation = re_findall('.*?"t4">(.*?)</span>', html)[0]
                        pub_date = re_findall('.*?"t5">(.*?)</span>', html)[0]

                        if job_url.find('jobs.51job')>=0:
                            print 'job_url 符合规则'

                            pub_time = str(s_date)[:4] + pub_date.replace('-', '')
                            print u'发布时间 : ' + pub_time

                            ptime = pub_time.encode('utf-8')
                            timestamp = get_timestamp(ptime)

                            start_timestamp = get_timestamp(s_date)

                            end_timestamp = start_timestamp + int(345600)


                            print job_url + u'  检测时间是否符合要求'
                            if start_timestamp <= timestamp < end_timestamp:
                                print job_url + u'  时间符合要求 '

                                cursor.execute('replace into 51job_single_url set job_url="%s",datestamp="%s"' %
                                               (
                                                   job_url,

                                                   str(datetime.datetime.now())[:10]

                                               ))
                                conn.commit()

                                # cursor.execute(
                                #     'insert into 51job_career_list_copy values ("%s","%s","%s","%s","%s","%s","%s","%s","%s")' %
                                #     (
                                #         job_url
                                #         # , job_name
                                #         # , company_url
                                #         # , company_name
                                #         # , salary
                                #         # , lcation
                                #         # , pub_date
                                #         # , str(datetime.datetime.now())
                                #         , str(datetime.datetime.now())[:10]
                                #     )
                                # )
                                # conn.commit()
                                print u'插入成功  ' + str(datetime.datetime.now())
                            else:
                                # cursor.execute('insert into 51job_error_log values("%s","%s","%s","%s")' % (
                                #     job_url, e, '时间不符合要求', str(datetime.datetime.now())))
                                # conn.commit()
                                if start_timestamp > timestamp:
                                    print job_url + u'  时间不符合要求 '
                                    flag=0
                                    break
                                # 上面的flag 就是指 在检测到时间不符的数据时 接下来的数据都是不符的 所以跳出for循环 开始下一个页面

                            break
                        else:
                            print ' 不符合规则的job_url  ' + str(job_url)
                            break
                    except Exception, e:
                        print str(e)
                        if str(e).find('2006') >= 0:
                            conn = MySQLdb.connect(host="139.198.189.129", port=20009, user="root", passwd="somao1129",
                                                  db="51job",
                                                  charset="utf8")
                            cursor = conn.cursor()
                            continue
                        else:
                            break
                i += 1
            break
        except Exception,e:
            print u'最外层'+str(e)
            break



def main():
    # test_url = 'http://search.51job.com/list/000000,000000,0000,00,9,01,%2B,2,1.html?lang=c&stype=1&postchannel=0000&workyear=01&cotype=99&degreefrom=01&jobterm=99&companysize=01&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    s_date = input('Start from (input like this : YYYYMMDD):')
    main_urls = get_main_urls()
    # main_urls = [
    #     'http://search.51job.com/list/000000,000000,0000,00,9,01,%2B,2,1.html?lang=c&stype=1&postchannel=0000&workyear=01&cotype=99&degreefrom=01&jobterm=99&companysize=01&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',
    #     'http://search.51job.com/list/000000,000000,0000,00,9,01,%2B,2,2.html?lang=c&stype=1&postchannel=0000&workyear=01&cotype=99&degreefrom=01&jobterm=99&companysize=01&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',
    #     'http://search.51job.com/list/000000,000000,0000,00,9,01,%2B,2,3.html?lang=c&stype=1&postchannel=0000&workyear=01&cotype=99&degreefrom=01&jobterm=99&companysize=01&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',
    #     'http://search.51job.com/list/000000,000000,0000,00,9,01,%2B,2,4.html?lang=c&stype=1&postchannel=0000&workyear=01&cotype=99&degreefrom=01&jobterm=99&companysize=01&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',
    #     'http://search.51job.com/list/000000,000000,0000,00,9,01,%2B,2,5.html?lang=c&stype=1&postchannel=0000&workyear=01&cotype=99&degreefrom=01&jobterm=99&companysize=01&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=']

    for detail_urls in main_urls:
        every_main_urls = get_detail_urls(detail_urls)
        for url in every_main_urls:
            get_data(url, s_date)
