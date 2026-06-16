import re
from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

vector = pickle.load(open("vectorizer.pkl", "rb"))
model = pickle.load(open("phishing.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        # print(url)
        
        cleaned_url = re.sub(r'^https?://', '', url)
        print(cleaned_url)
        
        predict = model.predict(vector.transform([cleaned_url]))
        # print(predict)
        
        if predict == 'bad':
            predict = "This is a phishing website !!!"
        elif predict == 'good':
            predict = "This is a legitimate website."
        else:
            predict = "Something went wrong. Please try again."
        
        return render_template("index.html", predict=predict)
    
    else: 
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)