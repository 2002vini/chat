from django import forms

class MyForm(forms.Form):
    pattern=forms.CharField(max_length=50)
    user_count=forms.IntegerField()
    password=forms.CharField(widget=forms.PasswordInput)
    