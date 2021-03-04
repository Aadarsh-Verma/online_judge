from django.contrib import admin

# Register your models here.
from judge.models import Question, TestCase

admin.site.register(Question)
admin.site.register(TestCase)