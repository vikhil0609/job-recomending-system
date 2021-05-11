from flask import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


app = Flask(__name__)

@app.route('/')
def json():
    return render_template('index.html')

#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
	PATH = "C:\web_drivers\chromedriver.exe"
	driver = webdriver.Chrome(PATH)

	driver.get("https://in.indeed.com")
	print(driver.title)

	search = driver.find_element_by_id("text-input-what")
	search.send_keys("web developer")
	search.send_keys(Keys.RETURN)

	return ("NOTHING")


if __name__ == '__main__':
	app.run(debug=True)