import os
import sys
from flask import Flask, flash, redirect, render_template, request, session, abort
from main_model import Main_Model
from flask_ngrok import run_with_ngrok
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from IPython.display import Javascript

app = Flask(__name__)
run_with_ngrok(app)  

def train_model():
    global model

    print("Train the model")
    model = Main_Model()

@app.route("/")
@app.route("/main")
def index():
    return render_template('index.html')


@app.route('/result',methods = ['POST', 'GET'])
def result():
    global result
    if request.method == 'POST':
		    descripton = request.form['Job']
		    processed_text = model.prediction(descripton)
		    result = processed_text
		    return render_template("result.html",result=result)
    else:
		    return render_template("index.html")
def clear_bash():
    os.system('cls' if os.name == 'nt' else 'clear')


def open_web(url):
    display(Javascript('window.open("{url}");'.format(url=url)))

@app.route('/background_process_test')
def background_process_test():
    sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
    driver.get("https://in.indeed.com")
    print(driver.title)

    search = driver.find_element_by_id("text-input-what")
    search.send_keys(result)
    search.send_keys(Keys.RETURN)

    # Getting current URL
    url = driver.current_url

    open_web(url)  


    return ("NOTHING")


if __name__ == "__main__":
    clear_bash()
    train_model()
    app.run()


