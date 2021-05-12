from flask import *


app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html")

@app.route("/result",methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
		descripton = request.form['Job']
		train_model()
		processed_text = model.prediction(descripton)
		result = processed_text
		return render_template("result.html",result=result)
	else:
		return render_template("index.html")

if __name__ == '__main__':
	app.run()