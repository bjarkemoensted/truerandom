
from flask import Flask, render_template, url_for, request, session, redirect
import os
import true_random

img_path = os.path.join("static", "img")


app = Flask(__name__, static_url_path='/static')
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
        else:
            toss = "tails"
            pic = os.path.join(img_path, "qtails.jpg")

    return render_template("coin.html", toss=toss, pic=pic)


@app.route('/dice', methods=['GET', 'POST'])
def dice():
    roll = ""
    error = ""
    lower = "1"
    upper = "6"
    if request.method == "POST":
        try:
            low = int(request.values.get('lower'))
            high = int(request.values.get('upper'))
            n = true_random.qrandint(low=low, high=high)
            lower = str(low)
            upper = str(high)
            roll = str(n)
        except ValueError:
            error = "Couldn't parse that!"
            roll = ""
        #
    else:
        n = true_random.qrandint(low=int(lower), high=int(upper))
        roll = str(n)

    return render_template("dice.html", roll=roll, error=error,
                           lower=lower, upper=upper)


@app.route('/choice', methods=['GET'])
def choice():
    return render_template("choice.html")


if __name__ == '__main__':
    app.run(debug=True)