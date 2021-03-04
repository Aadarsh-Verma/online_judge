from django import forms

from judge.models import Question


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'


