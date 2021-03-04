from django.db import models


# Create your models here.

class Question(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=250)
    problem = models.TextField()

    def __str__(self):
        return self.name


class TestCase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='question')
    text = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question.name + " " + str(self.id) + " " + self.question.code
