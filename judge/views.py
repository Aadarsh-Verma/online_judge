from django.http import JsonResponse
from django.shortcuts import render
import requests
# Create your views here.
from django.views.decorators.csrf import csrf_exempt


def get_output(code_part, input_part):
    RUN_URL = u'https://api.hackerearth.com/v3/code/run/'
    CLIENT_SECRET = '846b9673047638b7626eeb9dc65022312791cb44'

    data = {
        'client_secret': CLIENT_SECRET,
        'async': 0,
        'source': code_part,
        'input': input_part,
        'lang': "PYTHON3",
        'time_limit': 5,
        'memory_limit': 262144,
    }
    r = requests.post(RUN_URL, data=data)
    return r.json()

def index(request):
    context = {}
    return render(request, 'problem/problem.html', context)

@csrf_exempt
def runcode(request):
    print("runcode called")
    if request.method == 'POST':
        code_part = request.POST['code']
        input_part = request.POST['input']
        output = get_output(code_part,input_part)
        print(output['run_status'])
        return JsonResponse({'data': output['run_status']})
