from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Edge()
driver.get("https://www.baidu.com")
assert "百度" in driver.title
elem = driver.find_element_by_id("kw")
elem.clear()
elem.send_keys("股票系统")
elem.send_keys(Keys.RETURN)
time.sleep(5)

while 1:
    if "www.s-mo.com" in driver.page_source:
        for weblink in driver.find_elements_by_class_name("result c-container "):
            if "www.s-mo.com" in weblink.text:
                weblink.find_element_by_class_name("t").click()
                time.sleep(5)
                break
        break
    else:
        driver.find_element_by_link_text("下一页>").click()
        time.sleep(5)

time.sleep(5)

driver.quit()