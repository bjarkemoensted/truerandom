
from flask import Flask, render_template, url_for, request, session, redirect
import os
import true_random

img_path = os.path.join("static", "img")


app = Flask(__name__)
app.secret_key = "superdupersecretkey"


@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")

@app.route('/coin', methods=['GET', 'POST'])
def coin():
    toss = None
    pic = None
    if request.method == 'GET':
        toss = "superposition"
        pic = os.path.join(img_path, "superpos.jpg")
    else:
        tossisheads = true_random.qbool()
        if tossisheads:
            toss = "heads"
            pic = os.path.join(img_path, "qheads.jpg")
            #pic = "qheads.jpg"
        else:
            toss = "tails"
            pic = os.path.join(img_path, "qtails.jpg")
    return render_template("coin.html", toss=toss, pic=pic)

if __name__ == '__main__':
    app.run(debug=True)