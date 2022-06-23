from django import forms

from .models import *

class registrationsForm(forms.ModelForm):


    class Meta:
        model = Participant
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input_text', 'type': 'text', 'placeholder': 'ФИО*'}),
            'emailadress': forms.TextInput(attrs={'class': 'input_text', 'type': 'text', 'placeholder': 'Email*'}),
            'phonenumber': forms.TextInput(attrs={'class': 'input_text', 'type': 'text', 'placeholder': 'Телефон*'}),
            'organization': forms.TextInput(attrs={'class': 'input_text', 'type': 'text', 'placeholder': 'Организация*'}),
            'university_faculty': forms.TextInput(attrs={'class': 'input_text', 'type': 'text', 'placeholder': 'Факультет'}),
            'university_course': forms.TextInput(attrs={'class': 'input_text', 'type': 'text', 'placeholder': 'Курс'}),
        }