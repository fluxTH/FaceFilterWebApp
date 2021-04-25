#!/usr/bin/env python3

from flask import Flask, render_template
import config

app = Flask(
    config.APP_NAME, 
    template_folder='./frontend',
    static_folder='./frontend/static',
)

@app.route("/")
def root():
    return render_template('index.html')

if __name__ == "__main__":
    # run debug server
    app.run(host='127.0.0.1', port=5050, debug=True)