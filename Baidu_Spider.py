# coding:utf-8
"""
Created on 2018年1月4日
@author: AlexDu
@version: 1.1
@copyright: IT运维经验.
@license: GPLv3

"""

import logging
import time
from bs4 import BeautifulSoup
import requests
baidu_requests_session = requests.session()


class GetKeyWordUrl:

    def __init__(self, dic):
        self.key_word = dic['keyword']
        self.site_url = dic['url']
        logging.info("优化关键词{}".format(self.key_word))
        logging.info("优化针对的URL:{}".format(self.site_url))

    def __get_proxy(self, proxy):
        self.__proxies = {"http": "http://{}".format(proxy),
                          "https": "http://{}".format(proxy)
                          }

    def __matching(self, data):
        if self.site_url in data:
            url = self.__get_match_url(data, "https://www.qnjslm.com/")
            return True, url
        else:
            url = self.__get_match_url(data, "下一页>")
            return False, "https://www.baidu.com" + url

    @staticmethod
    def __get_match_url(data, keyword):
        soup = BeautifulSoup(data, "html.parser")
        for link in soup.find_all('a'):
            if keyword in link.get_text():
                return link.get('href')
        return None

    def __get_url(self, ua):
        match_url = "https://www.baidu.com/s?cl=3&ie=utf-8&wd=%s" % self.key_word
        count_num = 0
        try:
            referer_url = 'https://www.baidu.com'
            while count_num < 76:
                response = baidu_requests_session.get(match_url, headers=self.__set_header(ua, referer=referer_url),
                                                      proxies=self.__proxies, timeout=10)
                count_num += 1
                referer_url = response.url
                (match_code, match_url) = self.__matching(response.text)
                if match_url is None:
                    return 14, "没有找到相关的下一页连接,或者页面无法打开"
                if match_code:
                    # 找到网站连接
                    logging.info("找到关键词'%s',在百度搜索第'%s'页,URL访问连接:%s" % (self.key_word, count_num, match_url))
                    baidu_requests_session.get(match_url, headers=self.__set_header(ua, referer=referer_url),
                                               proxies=self.__proxies, timeout=10)
                    return 10, match_url
                else:
                    # 没有找到网站连接，进行下一页查找
                    logging.info("没有找到关键词'%s',在百度搜索第'%s'页" % (self.key_word, count_num))
                    time.sleep(3)
            else:
                logging.warning("放弃吧！你的关键词在搜索中没有找到")
        except requests.exceptions.ConnectionError:
            # 抓取失败，再次进行抓取
            return 11, "百度页面无法打开"
        except requests.exceptions.Timeout:
            return 13, "连接超时，还请尝试更换代理"

    def __access_site(self, url, ua):
        import random
        try:
            response = baidu_requests_session.get(url, headers=self.__set_header(ua, url), proxies=self.__proxies)
            for i in range(1, random.randint(2, 15)):
                inside_url_list = self.__get_site_match_url(response.text)
                url_random = random.randint(0, len(inside_url_list) - 1)
                inside_url = inside_url_list[url_random]
                time.sleep(random.randint(20, 60))
                r_url = response.url
                response = baidu_requests_session.get(inside_url, headers=self.__set_header(ua, r_url),
                                                      proxies=self.__proxies)
                logging.info("成功访问URL：%s" % inside_url)

        except requests.exceptions.ConnectionError:
            logging.warning("网站打开失败")

    def __get_site_match_url(self, data):
        soup = BeautifulSoup(data, "html.parser")
        inside_url = []
        for link in soup.find_all('a'):
            url = link.get('href')
            if url is not None:
                if self.site_url in url and 'go.php' not in url:
                    inside_url.append(url)
        return inside_url

    @staticmethod
    def __set_header(ua, referer=''):
        headers = {
                   'User-Agent': ua,
                   'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                   'Referer': referer,
                   }
        return headers

    def man(self, proxy, ua):
        """
        code 说明
        10  百度爬取成功，返回相应的URL
        11  百度页面打开异常
        12  代理服务器连接失败
        13  连接服务器超时
        14  百度搜索页面失败，或者没有下一页
        :return:
        """

        logging.info("优化使用代理服务器:{}".format(proxy))
        self.__get_proxy(proxy)
        (return_code, message) = self.__get_url(ua)
        if return_code == 10:
            logging.info("找到匹配的URL连接:{}".format(message))
            self.__access_site(message, ua)
        elif 11 <= return_code <= 14:
            logging.critical(message)
        return return_code, message
