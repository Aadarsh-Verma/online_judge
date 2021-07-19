from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from judge.forms import QuestionCreateForm
from judge.models import TestCase, Question, Contest, Submission
import requests


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
    print(r)
    return r.json()['run_status']


def index(request):
    context = {}
    return render(request, 'problem/problem.html', context)


@csrf_exempt
def runcode(request):
    print("runcode called")
    if request.method == 'POST':
        code_part = request.POST['code']
        input_part = request.POST['input']
        print(input_part)
        input_lang = request.POST['language']
        data = get_output(code_part, input_part, input_lang)
        print(data)
        return JsonResponse({'data': data})


def addTestCase(request):
    context = {}
    if request.method == 'POST':
        code = request.POST.get('code')
        answer = request.FILES['answer'].read()
        testcase = request.FILES['testcase'].read()
        print(testcase)
        answer = answer.decode("utf-8")
        testcase = testcase.decode("utf-8")
        print(testcase)
        question = Question.objects.get(code__exact=code)
        TestCase.objects.create(question=question, text=testcase, answer=answer)
        return redirect('home')
    return render(request, 'problem/AddTestCase.html', context)


@login_required
@csrf_exempt
def submitcode(request, code):
    print("submit code called")
    question = Question.objects.get(code__exact=code)
    if request.method == 'POST':
        code_part = request.POST['code']
        input_lang = request.POST['language']
        testcases = TestCase.objects.filter(question=question)
        result = []

        submission_testcase = ""
        for i in range(0, len(testcases)):
            code_output = get_output(code_part, testcases[i].text, input_lang)
            print("code output is ")
            print(code_output)
            if code_output['status'] == 'RE':
                Submission.objects.create(user=request.user, question=question, status="Runtime Error",
                                          testcase=submission_testcase, code=code_part, language=input_lang)
                return JsonResponse({'result': "Error in your Code:<br>" + code_output['stderr']})
            if code_output['status'] == 'CE':
                Submission.objects.create(user=request.user, question=question, status="Compile Error",
                                          testcase=submission_testcase, code=code_part, language=input_lang)
                return JsonResponse({'result': "Your Code Did Not Compile Successfully"})
            if judge(code_output['output'], testcases[i].answer):
                result.append("Test Case No {0} Passed<br>".format(i))
                submission_testcase += "Passed, "
            else:
                result.append("Test Case No {0} Failed<br>".format(i))
                submission_testcase += "Failed, "
        response = {'result': result}
        print(result)
        Submission.objects.create(user=request.user, question=question, status="AC",
                                  testcase=submission_testcase, code=code_part, language=input_lang)
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
    questions_set = Question.objects.all()
    submissions = Submission.objects.all()
    contests = Contest.objects.all()
    context = {
        'questions': questions_set,
        'contests': contests,
        'submissions': submissions,
    }

    return render(request, 'problem/home.html', context)


def ContestCreate(request):
    questions = Question.objects.all()
    if request.method == 'POST':
        form = request.POST
        name = form.get('name')
        start_time = form.get('start_time')
        duration = form.get('duration')
        contest = Contest.objects.create(name=name, start_time=start_time, duration=duration)

        return redirect('home')
    context = {'questions': questions}
    return render(request, 'judge/contest_create.html', context)


def addQuestion(request, pk):
    contest = Contest.objects.get(id=pk)
    question_set = Question.objects.all()
    if request.method == 'POST':
        question_ids = request.POST.getlist('question_ids')
        print(question_ids)
        question_set = []
        for q_id in question_ids:
            question_set.append(Question.objects.get(id=q_id))
        for question in question_set:
            contest.question.add(question)
        return redirect('home')
    context = {
        'questions': question_set
    }
    return render(request, 'judge/addQuestion.html', context)
