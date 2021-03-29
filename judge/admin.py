from django.contrib import admin

# Register your models here.
from judge.models import Question, TestCase, Contest, Participant, Submission

admin.site.register(Question)
admin.site.register(TestCase)
admin.site.register(Contest)
admin.site.register(Participant)
admin.site.register(Submission)
