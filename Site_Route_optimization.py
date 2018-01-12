# coding:utf-8
"""
Created on 2018年1月4日
@author: AlexDu
@version: 1.1
@copyright: IT运维经验.
@license: GPLv3

站点来路优化，模拟从其他网站进行跳转，并进行深度访问
"""
import requests
import logging
import random
import time
from bs4 import BeautifulSoup
site_requests_session = requests.session()


class SiteRouteOptimization:
    def __init__(self):
        pass

    def man(self, ua, url):
        logging.debug("进行来路访问，优化")

    def __access_website(self, url, ua, referer):
        try:
            response = site_requests_session.get(url, headers=self.__set_headers(ua, referer), proxies=self.__proxies)
            for i in range(1, random.randint(2, 15)):
                inside_url_list = self.__get_site_match_url(response.text)
                if inside_url_list is None:
                    logging.warning("在页面上没有找到指定的地址，结束访问")
                    return
                url_random = random.randint(0, len(inside_url_list) - 1)
                inside_url = inside_url_list[url_random]
                time.sleep(random.randint(20, 60))
                response = site_requests_session.get(inside_url, headers=self.__set_header(r_url), proxies=self.__proxies)
                r_url = inside_url
                logging.info("成功访问URL：%s" % inside_url)

        except requests.exceptions.ConnectionError:
            logging.critical("网站打开失败")
        except requests.exceptions.ProxyError:
            logging.critical("代理失效结束访问")

    @staticmethod
    def route_url():
        route_list = [
            'http://blog.sina.com.cn/',
            'http://www.it168.com/',
            'http://blog.csdn.net/',
            'https://www.ithome.com/',
            'https://it.ithome.com/',
            'http://www.pconline.com.cn/',
            'https://www.itjuzi.com/',
            'http://www.51cto.com/']
        return random.choice(route_list)

    @staticmethod
    def __set_headers(ua, referer):
        headers = {
            'User-Agent': ua,
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Referer': referer,
            'Upgrade-Insecure-Requests': '1'
        }
        return headers

    @staticmethod
    def __proxies():
        pass

    @staticmethod
    def __get_site_match_url(data, mach="https://www.qnjslm.com"):
        soup = BeautifulSoup(data, "html.parser")
        for link in soup.find_all('a'):
            if mach in link.get_text():
                return link.get('href')
        return None
