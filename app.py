
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
        n = true_random.randint(low=int(lower), high=int(upper))
        roll = str(n)

    return render_template("dice.html", roll=roll, error=error,
                           lower=lower, upper=upper)


def make_choicelist(picks):
    template = '''
        <p class="boxThing volatile">
				%s
		  </p>'''

    font_size = 42
    diva = '<div>'
    if len(picks) != 1:
        diva = '<div class="simplePad" style="font-size:%dpx">' % font_size

    divb = '</div>'
    formatted = [p+", " for p in picks[:-1]] + [picks[-1]]
    html = "\n".join((diva + s + divb) for s in formatted)
    res = template % html

    return res




@app.route('/choice', methods=['GET', 'POST'])
def choice():
    error = ''
    pick = ''
    size = 1
    candidates_string = ''

    if request.method == 'POST':
        try:
            raw = request.values.get("list")
            size = int(request.values.get("size"))
            arr = [s.strip() for s in raw.strip().split(",") if s.strip()]
            candidates_string = ", ".join(sorted(arr))
            picks = true_random.choice(a=arr, size=size, replace=False)

            pick = make_choicelist(picks)
        except ValueError:
            error = "Parsing error. Make sure to enter a comma-separated list."

    return render_template("choice.html", error=error, size=str(size),
                           candidates_string=candidates_string, pick=pick)


if __name__ == '__main__':
    app.run(debug=True)