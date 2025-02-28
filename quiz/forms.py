from django import forms

class QuizAnswerForm(forms.Form):
    answer = forms.CharField(label="Your Answer", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
