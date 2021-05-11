from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://in.indeed.com")
print(driver.title)

search = driver.find_element_by_id("text-input-what")
search.send_keys("web developer")
search.send_keys(Keys.RETURN)


# driver.close() To close a tab
# driver.quit() To close the whole window