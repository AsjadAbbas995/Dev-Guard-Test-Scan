# DELIBERATELY INSECURE - scanner test fixture. Do not use.
import os
import pickle
import sqlite3
import subprocess

from flask import Flask, request

app = Flask(__name__)


@app.route('/run')
def run():
    cmd = request.args.get('cmd', '')
    return subprocess.check_output(cmd, shell=True)          # command injection


@app.route('/calc')
def calc():
    return str(eval(request.args.get('expr', '1')))          # eval of user input


@app.route('/user')
def user():
    name = request.args.get('name', '')
    conn = sqlite3.connect('app.db')
    cur = conn.execute("SELECT * FROM users WHERE name = '%s'" % name)  # SQL injection
    return str(cur.fetchall())


@app.route('/load', methods=['POST'])
def load():
    return str(pickle.loads(request.data))                   # insecure deserialisation


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)                      # debug server exposed
