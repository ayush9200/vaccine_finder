# Ayush Kumar Singh (C0799530) flask
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/home")
def index():
    return render_template('homepage.html')

if __name__ == "__main__":
    app.run()