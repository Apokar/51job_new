# -*- coding: utf-8 -*-
# @Time         : 2017/11/21 09:51
# @Author       : Huaiz
# @Email        : Apokar@163.com
# @File         : run.py
# @Software     : PyCharm Community Edition
# @PROJECT_NAME : 51job_new
import threading

from Job51_detail import *
from Job51_list import *

s_date = input('Start from (input like this : YYYYMMDD):')
while True:
    print u'处理列表页 _@_ ' + str(datetime.datetime.now())
    main_urls = get_main_urls()
    for detail_urls in main_urls:
        every_main_urls = get_detail_urls(detail_urls)
        for url in every_main_urls:
            get_data(url, s_date)

    #>>>>>>>>>>>>>>>>>>可以单独运行的部分 start  >>>>>>>>>>>
    print u'处理详情页 _@_ ' + str(datetime.datetime.now())
    need_urls = get_detail_pages()
    # for url in need_urls:
    #     get_info(url)
    start_no = 0
    thread_num=10

    end_no = len(need_urls)

    while start_no < (end_no - thread_num + 1):
        threads = []

        for inner_index in range(0, thread_num):
            threads.append(threading.Thread(target=get_info, args=(need_urls[start_no + inner_index],)))
        for t in threads:
            t.setDaemon(True)
            t.start()
        t.join()
        start_no += thread_num
    # >>>>>>>>>>>>>>>>>>可以单独运行的部分 end  >>>>>>>>>>>

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