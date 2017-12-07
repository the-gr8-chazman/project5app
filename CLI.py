import sys
import requests

try:
    restmethod = sys.argv[1]
    restarg = sys.argv[2]
except:
    restmethod = "null"
    if restmethod == 'null':
        sys.exit("CLI.py <REST URL> <integer/string/key> <if kv-record, value> <if kv-record, identify PUT or POST")
try:
    value = sys.argv[3]
    putpost = sys.argv[4]
except IndexError:
    value = 'null'
    method = 'null'

if  restmethod not in {"md5", "factorial", "fibonacci", "is-prime", "slack-alert", "kv-record", "kv-retrieve"}: 
    (sys.exit("incorrect rest method/ url path"))

rest = "http://0.0.0.0:5000/"+restmethod+"/"+restarg 
kv = "http://0.0.0.0:5000/"+restmethod+"/"

if restmethod == "kv-record":
   data = {restarg:value}
   if putpost.lower() == 'post':
           resp = requests.post(kv, json=data)
           #print resp
   elif putpost.lower() == 'put':
           resp = requests.put(kv, json=data)
   else:
           sys.exit("<REST URL> <integer/string/key> <if kv-record, value> <if kv-record, identify PUT or POST")

else:
    resp = requests.get(rest)

print resp.content


