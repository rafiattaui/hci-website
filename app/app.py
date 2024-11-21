from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "<h4>Hello, this is the main page!</h4>"

if __name__ == '__main__':
    app.run()