from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from judge.forms import QuestionCreateForm
from judge.models import TestCase, Question


def judge(code_output, correct_output):
    code_output = code_output.splitlines()

    testcase = correct_output
    testcase_output = "".join(testcase)
    testcase_output = testcase_output.splitlines()

    if len(code_output) != len(testcase_output):
        return False

    for i in range(0, len(code_output)):
        if code_output[i] != testcase_output[i]:
            return False
    return True


def get_output(code_part, input_part, input_lang):
    RUN_URL = u'https://api.hackerearth.com/v3/code/run/'
    CLIENT_SECRET = '846b9673047638b7626eeb9dc65022312791cb44'
    language = ""
    if input_lang == 'c_cpp':
        language = "CPP14"
    if input_lang == "java":
        language = "JAVA8"
    if input_lang == "python":
        language = "PYTHON3"

    data = {
        'client_secret': CLIENT_SECRET,
        'async': 0,
        'source': code_part,
        'input': input_part,
        'lang': language,
        'time_limit': 5,
        'memory_limit': 262144,
    }
    r = requests.post(RUN_URL, data=data)
    return r.json()['run_status']['output']


def index(request):
    context = {}
    return render(request, 'problem/problem.html', context)


@csrf_exempt
def runcode(request):
    print("runcode called")
    if request.method == 'POST':
        code_part = request.POST['code']
        input_part = request.POST['input']
        input_lang = request.POST['language']
        output = get_output(code_part, input_part, input_lang)
        print(output)
        return JsonResponse({'data': output})


def addTestCase(request):
    context = {}
    if request.method == 'POST':
        code = request.POST.get('code')
        answer = request.FILES['answer'].read()
        testcase = request.FILES['testcase'].read()
        print(answer)
        answer = answer.decode("utf-8")
        testcase = testcase.decode("utf-8")
        print(answer)
        print(len(answer))
        question = Question.objects.get(code__exact=code)
        TestCase.objects.create(question=question, text=testcase, answer=answer)
        return redirect('home')
    return render(request, 'problem/AddTestCase.html', context)


@csrf_exempt
def submitcode(request, code):
    print("submit code called")
    question = Question.objects.get(code__exact=code)
    if request.method == 'POST':
        code_part = request.POST['code']
        input_lang = request.POST['language']
        testcases = TestCase.objects.filter(question=question)
        result = []
        for i in range(0, len(testcases)):
            code_output = get_output(code_part, testcases[i].text, input_lang)
            print(code_output)
            if judge(code_output, testcases[i].answer):
                result.append("Test Case No {0} Passed<br>".format(i))
            else:
                result.append("Test Case No {0} Failed<br>".format(i))
        response = {'result': result}
        print(result)
        return JsonResponse(response)

    context = {'question': question}
    return render(request, 'problem/QuestionPage.html', context)


def createQuestion(request):
    form = QuestionCreateForm()
    if request.method == 'POST':
        form = QuestionCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'problem/QuestionCreateForm.html', {'form': form})


def home(request):
    questions = Question.objects.all()
    context = {'questions': questions}

    return render(request, 'problem/home.html', context)
