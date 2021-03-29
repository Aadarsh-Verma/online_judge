import requests

# constants
RUN_URL = u'https://api.hackerearth.com/v3/code/run/'
CLIENT_SECRET = '846b9673047638b7626eeb9dc65022312791cb44'

file_object = open("a.py","r")
code_loop = file_object.readlines()

source = "prindt(4.5)"


data = {
    'client_secret': CLIENT_SECRET,
    'async': 0,
    'source': source,
    'input' : 17,
    'lang': "PYTHON",
    'time_limit': 5,
    'memory_limit': 262144,
}

r = requests.post(RUN_URL, data=data)
print(r.json())
print(r.json()['run_status']['status']!='AC')
code_output = r.json()['run_status']['output']
print(code_output)