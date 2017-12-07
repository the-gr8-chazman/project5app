from flask import Flask, request, json
import json, requests, config, math, redis


app = Flask(__name__)

db = redis.Redis('redis')


@app.route('/')
def hello_world():
    return "Hello, welcome to my API application"


@app.route('/md5/<path:inp>')
def hash(inp):
	import md5
	m = md5.new()
	m.update(inp.encode('utf-8'))
	out =  m.hexdigest()
	return json.dumps({"input":inp, "output":out})


@app.route('/factorial/<int:inp>')
def fact(inp):
	try:
		if inp < 0:
			raise ValueError()
	except ValueError:
		return json.dumps({"input":inp, "output":"Value must be a non-negative integer"}) 
	else:
		out = math.factorial(inp);
		return json.dumps({"input":inp, "output":out})


@app.route('/fibonacci/<int:inp>')
def fibonacci(inp):
	try:
		if inp <= 0:
			raise ValueError()
	except ValueError:
		return json.dumps({"input":inp, "output":"Value must be a non-negative integer"}) 
	else:
		final = inp
		out = [0, 1, 1]
		i = 0
		while (out[-1]+out[-2]) <= final:
			i = out[-1] + out[-2] 
			out.append(i)
		return json.dumps({"input":inp, "output":out})


@app.route('/is-prime/<int:inp>')
def isPrime(inp):
        try:
                if inp <= 0:
                        raise ValueError()
        except ValueError:
                return json.dumps({"input":inp, "output":"Value must be an integer, greater than 0"}) 
        else:
		num = inp
		check = 1
		for i in range(2, num-1):
			if num % i == 0:
            			check = 0
		if inp == 1:
			check = 0
		if check:
			return json.dumps({"input":inp, "output":True})
		else:
			return json.dumps({"input":inp, "output":False})


@app.route('/slack-alert/<string:inp>')
def slackAlert(inp):
	try:
		url = config.HOOK
		r = requests.post(url, data=json.dumps({'text':inp}),headers={'Content-Type': 'application/json'})
		return json.dumps({"input":inp, "output":True})
	except Exception as err:
		print(err)
		return json.dumps({"input":inp, "output":False})


@app.route('/kv-record/', methods = ["POST", "PUT"])
def record():
	try:
		data = request.json
		key, value = data.items()[0]

		if request.method == "POST":
			if db.exists(key):
				return json.dumps({"input":key, "output": False, "error": "Unable to add pair: key already exists."})
			else:
				db.set(key, value)
				return json.dumps({"input":key+' '+value, "output": True})

		elif request.method == "PUT":
			if db.exists(key):
				db.set(key, value)
				return json.dumps({"input":key+' '+value, "output": True})
			else:
				return json.dumps({"input":key, "output": False, "error": "Unable to update value: key does not exist."})
				
		else:
			raise
	except Exception as err:
		return json.dumps({"output": False, "error": err})
		

@app.route('/kv-retrieve/<string:key>')
def retrieve(key):
	try:
		if db.exists(key):
			return json.dumps({"WHATTHEHELL":key, "output": db.get(key)})
		else:
			return json.dumps({"WHATTHEHELL":key, "output": False, "error": "Unable to update value: key does not exist."})
			
	except Exception as err:
		return json.dumps({"output": False, "error": err})


if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')
