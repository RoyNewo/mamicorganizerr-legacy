import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# import Action chains
from selenium.webdriver.common.action_chains import ActionChains
from icecream import ic
from selenium.common.exceptions import NoSuchElementException
import json
import os
import zipfile

def main():
    # Setup chrome options
    PROXY = "brd-customer-hl_e0fc9f88-zone-isp_proxy1:b5veb1ajbf71@brd.superproxy.io:22225"
    PROXY_HOST = 'brd.superproxy.io'  # rotating proxy or host
    PROXY_PORT = 22225 # port
    PROXY_USER = 'brd-customer-hl_e0fc9f88-zone-isp_proxy1' # username
    PROXY_PASS = 'b5veb1ajbf71' # password
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
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
    pluginfile = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    chrome_options.add_extension(pluginfile)
    # chrome_options.add_argument("--headless") # Ensure GUI is off
    # chrome_options.add_argument("--no-sandbox")
    # webdriver_service = Service("/home/cmgr003/onepace/chromedriver")
    # caps = webdriver.DesiredCapabilities.CHROME.copy() 
    # caps['acceptInsecureCerts'] = True

    # Web scrapper for infinite scrolling page #####
    # driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    driver = webdriver.Remote(command_executor='https://selenium.loyhouse.net/wd/hub', options=chrome_options)
    driver.get("https://es.ninemanga.com/manga/Kusuriya+no+Hitorigoto.html?waring=1")
    action = ActionChains(driver)
    time.sleep(5)  # Allow 2 seconds for the web page to open
    scroll_pause_time = 5  # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    chapterlistenlaces = driver.find_elements(By.CLASS_NAME, "chapter_list_a")
    print(chapterlistenlaces.text)
    driver.close()



if __name__ == "__main__":
    main()
