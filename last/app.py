from flask import Flask, request, make_response, jsonify
import json
import random, time, os, threading

app = Flask(__name__)

LOG_FILE = "operations.json"

@app.route('/reduce')
def reduce():
    op = request.args.get('op', type=str)
    lst = request.args.get('lst', type=str)
    if op and lst:
        lst = eval(lst)
        if op == 'add':
            res = sum(lst)
            response =  make_response(jsonify(s=res), 200)
        elif op == 'sub':
            res = lst[0] - sum(lst[1:])
            response = make_response(jsonify(s=res), 200)
        elif op == 'mul':
            res = 1
            for i in lst:
                res *= i
            response = make_response(jsonify(s=res), 200)
        elif op == 'div':
            res = lst[0]
            for i in lst[1:]:
                if i == 0:
                    return make_response('Division by zero\n', 400)
                res /= i
            response = make_response(jsonify(s=res), 200)
        elif op == 'concat':
            res = ""
            for i in lst:
                res += i
            response = make_response(jsonify(s=res), 200)
        else:
            return make_response(f'Invalid operator: {op}', 400)
        save_last("reduce",(op,lst),res)
        return response
    else:
        return make_response('Invalid operator\n', 400)

@app.route('/crash')
def crash():
    def close():
        time.sleep(1)
        os._exit(0)
    thread = threading.Thread(target=close)
    thread.start()
    ret = str(request.host) + " crashed"
    return make_response(jsonify(s=ret), 200)

@app.route('/last')
def last():
    try:
        with open('last.txt', 'r') as f:
            return make_response(jsonify(s=f.read()), 200)
    except FileNotFoundError:
        return make_response('No operations yet\n', 404)
    
@app.route("/notify", methods=["POST"])
def notify():
    data = request.json
    with open(LOG_FILE, "a") as f:
        json.dump(data, f)
        f.write("\n")
    return jsonify({"message": "Saved"}), 200


def save_last(op,args,res):
    with open('last.txt', 'w') as f:
            f.write(f'{op}{args}={res}')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
