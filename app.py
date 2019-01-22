
from flask import Flask, render_template, url_for, request, session, redirect


app = Flask(__name__)
app.secret_key = "superdupersecretkey"


@app.route('/', methods=['GET'])
def index():
    return "Testing..."


if __name__ == '__main__':
    app.run(debug=True)