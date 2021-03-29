from django.contrib.auth.models import User
from django.db import models

# Create your models here.
level = (('HARD','HARD'),('EASY','EASY'),('MEDIUM','MEDIUM'))


class Question(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=250)
    problem = models.TextField()
    difficulty = models.CharField(max_length=10,choices=level,blank=True)
    points = models.IntegerField(default=0,blank=True)

    def __str__(self):
        return self.name


class TestCase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='question')
    text = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question.name + " " + str(self.id) + " " + self.question.code


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    testcase = models.CharField(max_length=200)
    code = models.TextField()
    language = models.CharField(max_length=15)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question.name

class Contest(models.Model):
    name = models.CharField(max_length=50)
    question = models.ManyToManyField(Question,blank=True)
    start_time = models.DateTimeField()
    duration = models.IntegerField(default=60)

    def __str__(self):
        return self.name+" "+str(self.start_time)[5:16]

class Participant(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest,on_delete=models.CASCADE)




