import sys

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt


def index(request):
    context = {}
    return render(request, 'problem/problem.html', context)


@csrf_exempt
def calculate(request):
    if request.method == "POST":
        code = request.POST
        print(code)

        return JsonResponse({'status': 1})
    else:
        return JsonResponse({'status': 0})


@csrf_exempt
def runcode(request):
    print("runcode called")
    if request.method == 'POST':
        code_part = request.POST['code']
        input_part = request.POST['input']
        y = input_part
        input_part = input_part.replace("\n", " ").split(" ")
        print(input_part[0])

        def input():
            a = input_part[0]
            del input_part[0]
            return a

        try:
            orig_stdout = sys.stdout
            sys.stdout = open('file.txt', 'w')
            exec(code_part)
            sys.stdout.close()
            sys.stdout = orig_stdout
            output = open('file.txt', 'r').read()
        except Exception as e:
            sys.stdout.close()
            sys.stdout = orig_stdout
            output = e
        print(output)
        return JsonResponse({'output': output})
