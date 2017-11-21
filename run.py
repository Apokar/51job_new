# -*- coding: utf-8 -*-
# @Time         : 2017/11/21 09:51
# @Author       : Huaiz
# @Email        : Apokar@163.com
# @File         : run.py
# @Software     : PyCharm Community Edition
# @PROJECT_NAME : 51job_new

from Job51_detail import *
from Job51_list import *
#
s_date = input('Start from (input like this : YYYYMMDD):')
while True:
    print u'处理列表页 _@_ ' + str(datetime.datetime.now())
    main_urls = get_main_urls()
    for detail_urls in main_urls:
        every_main_urls = get_detail_urls(detail_urls)
        for url in every_main_urls:
            get_data(url, s_date)

    print u'处理详情页 _@_ ' + str(datetime.datetime.now())
    need_urls = get_detail_pages()
    for url in need_urls:
        get_info(url)

    timeArray = time.strptime(str(s_date), "%Y%m%d")
    timestamp = time.mktime(timeArray)
    timestamp = timestamp + int(345600)
    print timestamp
    if timestamp > int(time.time()):
        print s_date
        print u'最新的一天了 缓一缓'
        quit()
    else:
        time_local = time.localtime(timestamp)
        s_date = time.strftime("%Y%m%d",time_local)

        print u'爬' + s_date + u'及其4天后的内容'