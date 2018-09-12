# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 08:54:20 2018

@author: keshav
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import zipfile

def main_chrome(exe_path,PROXY_HOST='',PROXY_PORT='',PROXY_USER='',PROXY_PASS=''):
    manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

    background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
          singleProxy: {
            scheme: "http",
            host: "%(host)s",
            port: parseInt(%(port)d)
          },
          bypassList: ["foobar.com"]
        }
      };
chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
function callbackFn(details) {
    return {
        authCredentials: {
            username: "%(user)s",
            password: "%(pass)s"
        }
    };
}
chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
    """ % {
        "host": PROXY_HOST,
        "port": PROXY_PORT,
        "user": PROXY_USER,
        "pass": PROXY_PASS,
    }


    pluginfile = 'proxy_auth_plugin.zip'

    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)

    co = Options()
    #co.binary_location = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    #disable-infobars
    co.add_extension(pluginfile)
    co.add_argument('start-maximized')
    co.add_argument('disable-infobars')
    driver = webdriver.Chrome(exe_path,chrome_options=co)
    driver.get("http://www.google.ie")
    return driver
#driver.quit()
    
if __name__ == '__main__':
    main_chrome()