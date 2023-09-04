# python
# -*- coding: UTF-8 -*-
"""
@Project ：auto_wjx 
@File    ：clash.py.py
@Author  ：kaikai
@Date    ：2023/9/3 20:02 
"""
import requests
import numpy as np
import json


fmt = "====== {} ======\n{}\n"


class Clash:
    # external_controller, secret 具体值应根据 clash 的配置文件 config.yaml 中的 external-controller 和 secret 来设置
    def __init__(self, external_controller: str, secret: str = None):
        self.external_controller = external_controller
        self.secret = secret

    @property
    def headers(self):
        return {'Authorization': f"Bearer {self.secret}", 'Content-Type': "application/json"} if self.secret else {}

    def get_proxies(self):
        return requests.get(f"{self.external_controller}/proxies", headers=self.headers).json()["proxies"]

    def get_proxy(self, selector):
        return requests.get(f"{self.external_controller}/proxies/{selector}", headers=self.headers).json()

    def get_proxy_delay(self, selector, url="http://google.com", timeout=2000):
        return requests.get(f"{self.external_controller}/proxies/{selector}/delay", headers=self.headers, params={'url': url, 'timeout': timeout}).json()

    def change_proxy(self, selector, node):
        return requests.put(f"{self.external_controller}/proxies/{selector}", headers=self.headers, json={"name": node})

    def auto_change_proxy(self, selector, delay=300):
        print(fmt.format("proxy", self.get_proxy(selector)))
        proxies = self.get_proxy(selector)["all"]
        loop = True
        while loop:
            name = proxies[np.random.randint(len(proxies))]
            print(fmt.format("proxy name", name))
            # print(fmt.format("random proxy", clash.get_proxy("一元机场")["all"]))
            self.change_proxy(selector, name)
            res = self.get_proxy_delay("Proxy")
            print(fmt.format("test delay", res))
            loop = 'message' in res or res['meanDelay'] > delay


if __name__ == "__main__":
    clash = Clash("http://127.0.0.1:49710", "2ec23a7c-b6a0-4244-ac01-6f6fa7c1c61d")
    # proxies = clash.get_proxies()
    # print(fmt.format("proxies keys", proxies.keys()))
    clash.auto_change_proxy("Proxy")