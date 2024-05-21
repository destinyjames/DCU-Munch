import email
from django import forms
from django.forms import ModelForm
from .models import *

""" def __init__(self, *args, **kwargs):
        # first call parent's constructor
                super(UserForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
                self.fields['dietary_req'].required = False """

class UserForm(ModelForm):
   class Meta:

        model = Account
        fields = ( 'sex', 'age', 'weight', 'height', 'activity_level', 'dietary_req')

      
        SEX = (
                ('M', 'Male'),
                ('F', 'Female'),
                )
      
        ACTIVITY = (
                (1.2, 'Sedentary: little or no exercise'),
                (1.375, 'Exercise 1-3 times/week'),
                (1.55, "Exercise 4-5 times/week"),
                (1.725, "Daily exercise or intense exercise 3-4 times/week"),
                (1.9, "Intense exercise 6-7 times/week")
                )

        dietary_req = forms.MultipleChoiceField(choices=ALLERGENS, required=False)
        widgets = {
            'sex': forms.Select(choices=SEX),
             'activity_level': forms.Select(choices=ACTIVITY),

        }

        labels = {
            "weight": 'Weight (KG)',
            "height": 'Height (CM)'
        }

class OrderForm(ModelForm):
    name = forms.CharField(label="Name", widget=forms.TextInput(attrs={'class': "aesthetic-windows-95-text-input", 'placeholder': 'Name', 'id': 'name'}))
    email = forms.EmailField()
    studentId = models.CharField( max_length=8)

    class Meta:
        model = Order
        fields = ['name', 'email', 'studentId' ]
