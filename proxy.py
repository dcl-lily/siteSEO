# coding:utf-8
"""
Created on 2018年1月4日
@author: AlexDu
@version: 1.1
@copyright: IT运维经验.
@license: GPLv3

获取代理IP地址和端口，并进行验证访问论坛地址是否可以
"""

import requests
import logging


class GetProxy:
    def __init__(self, par={}):
        self.__GetApi = par['proxy_api'] if'proxy_api' in par.keys() else "http://www.alexdu.cf:5010/get/"
        self.__Verification_url = par['ver_url'] if 'ver_url' in par.keys() else "https://www.qnjslm.com/ip.php"

    def get_proxy(self):
        try:
            proxy = requests.get(self.__GetApi).text
            logging.info("通过API获取到代理IP地址{}".format(proxy))
        except requests.exceptions.ConnectTimeout:
            logging.critical("代理API服务器访问超时,请确认代理")
            return False, "proxy API conn timeout"
        code = self.verifcation_url(proxy)
        return code, proxy

    @staticmethod
    def delete_proxy(proxy):
        logging.info("删除代理{}".format(proxy))
        requests.get("http://www.alexdu.cf:5010/delete/?proxy={}".format(proxy))

    @staticmethod
    def verifcation_url(proxy):
        try:
            comm = requests.get("https://www.qnjslm.com/ip.php", timeout=6, proxies={'https': 'http://{}'.format(proxy)}).text
            if comm.strip() in proxy:
                logging.info("验证代理IP地址为:{},可以成功访问站点".format(comm.strip()))
            else:
                logging.warning("代理访问正常，但这可能是一个透明代理，IP地址:{}".format(comm.strip()))
            return True
        except requests.exceptions.ConnectTimeout:
            logging.warning("代理服务器连接超时")
            return False
        except requests.exceptions.ProxyError:
            logging.warning("代理服务器无法使用")
            return False
