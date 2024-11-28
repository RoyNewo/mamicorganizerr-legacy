import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.proxy import Proxy
# import Action chains
from selenium.webdriver.common.action_chains import ActionChains
from icecream import ic

def webdriver_init():
    print (("Initializing hub ....."))
    SELENIUM_HUB = 'http://192.168.1.131:4444/wd/hub'
    PROXY = '192.168.1.131:8118'
    options = FirefoxOptions()
    options.proxy = Proxy({
        "httpProxy": PROXY,
        "sslProxy": PROXY,
        "noProxy": None,
        "proxyType": "MANUAL",
        "class": "org.openqa.selenium.Proxy",
        "autodetect": False
    })
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Remote(
            command_executor=SELENIUM_HUB,
            options=options,
        )
    print (("Driver initalized..."))
    return driver

def webdriver_del(driver):
    driver.quit()

def main():
    
    driver = webdriver_init()
    driver.get("http://es.ninemanga.com/manga/Kusuriya+no+Hitorigoto.html")
    action = ActionChains(driver)
    time.sleep(5)  # Allow 2 seconds for the web page to open
    scroll_pause_time = 5  # You can set your own pause time. My laptop is a bit slow so I use 1 sec
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    chapterlistenlaces = driver.find_elements(By.CLASS_NAME, "chapter_list_a")
    # for enlance in chapterlistenlaces:
    #     print(enlance.text)
    chapterlistenlaces[0].click()
    time.sleep(60)
    driver.back()
    time.sleep(5)
    driver.quit()



if __name__ == "__main__":
    main()
