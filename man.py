# coding:utf-8
"""
Created on 2018年1月4日
@author: AlexDu
@version: 1.1
@copyright: IT运维经验.
@license: GPLv3
"""
import sys
import time
import proxy
import Baidu_Spider
import Get_UA
import logging
from logging.handlers import RotatingFileHandler
import os

curr_dir = os.path.dirname(os.path.realpath(__file__))
curr_dir = curr_dir + os.sep
LOG_FILE = curr_dir + 'SiteSeo.log'
handler = RotatingFileHandler(LOG_FILE, maxBytes=1024*1024, backupCount=5)
fmt = '%(asctime)s - %(levelname)s - %(filename)s[%(lineno)s] - %(threadName)s - %(message)s'
formatter = logging.Formatter(fmt)   # 实例化formatter
handler.setFormatter(formatter)      # 为handler添加formatter
logger = logging.getLogger('')    # 获取名为weixin的logger
logger.addHandler(handler)           # 为logger添加handler
logger.setLevel(logging.DEBUG)    #设置日志保存级别

# 打印到屏幕设定
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logger.addHandler(console)
logging.debug("程序启动,初始化完成")

logging.info("开始百度优化访问")
p_dic = {'keyword': 'IT运维经验', 'url': 'www.qnjslm.com'}
baidu_spider = Baidu_Spider.GetKeyWordUrl(p_dic)
sro = Get_UA.get_user_agent()
proxy = proxy.GetProxy()
while 1:
    (proxy_code, proxy_ip) = proxy.get_proxy()
    if proxy_code:
        if "no proxy" in proxy_ip:
            logging.warning("IP地址池没有可用代理IP地址，暂停等待")
            time.sleep(120)

        (baidu_code, baidu_message) = baidu_spider.man(proxy, sro)
        if baidu_code == 10:
            sys.exit(1)
        else:
            proxy.delete_proxy(proxy_ip)
    else:
        proxy.delete_proxy(proxy_ip)

