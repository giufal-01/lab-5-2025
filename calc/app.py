from flask import Flask, request, make_response, jsonify
import random, time, os, threading

app = Flask(__name__)


LAST_SERVICE_URL = "http://last:5002/notify"

@app.route('/add')
def add():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a and b:
        save_last("add",(a,b),a+b)
        return make_response(jsonify(s=a+b), 200) #HTTP 200 OK
    else:
        return make_response('Invalid input\n', 400) #HTTP 400 BAD REQUEST

@app.route('/sub')
def sub():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a and b:
        save_last("sub",(a,b),a-b)
        return make_response(jsonify(s=a-b), 200)

@app.route('/mul')
def mul():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a and b:
        save_last("mul",(a,b),a*b)
        return make_response(jsonify(s=a*b), 200)
    else:
        return make_response('Invalid input\n', 400)

@app.route('/div')
def div():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a and b:
        if b == 0:
            return make_response('Division by zero\n', 400)
        save_last("div",(a,b),a/b)
        return make_response(jsonify(s=a/b), 200)
    else:
        return make_response('Invalid input\n', 400)

@app.route('/mod')
def mod():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a and b:
        if b == 0:
            return make_response('Division by zero\n', 400)
        save_last("mod",(a,b),a%b)
        return make_response(jsonify(s=a%b), 200)
    else:
        return make_response('Invalid input\n', 400)


@app.route('/last')
def last():
    try:
        with open('last.txt', 'r') as f:
            return make_response(jsonify(s=f.read()), 200)
    except FileNotFoundError:
        return make_response('No operations yet\n', 404)


def save_last(op,args,res):
    with open('last.txt', 'w') as f:
            f.write(f'{op}{args}={res}')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)