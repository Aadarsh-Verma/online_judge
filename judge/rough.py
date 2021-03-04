from judge.models import TestCase
from judge.models import Question

testcases = TestCase.objects.all()[0]
output = testcases.answer
print(len(output))
print(output)
