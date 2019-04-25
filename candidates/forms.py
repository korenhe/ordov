from django import forms
from django_countries.fields import LazyTypedChoiceField
from django_countries import countries
from phonenumber_field.modelfields import PhoneNumberField
from ordov.choices import (EDUCATION_CHOICES,
	 GENDER_CHOICES)

class UserApplyStep1Form(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=50)
    phone = forms.CharField(max_length=12)

class UserApplyStep2Form(forms.Form):
    birth_year = forms.IntegerField(min_value=1950, max_value=2000)
    gender = forms.TypedChoiceField(choices=GENDER_CHOICES)
    education = forms.TypedChoiceField(choices=EDUCATION_CHOICES)
    education_major = forms.CharField(max_length=50)
    """
    image = forms.ImageField()
    resume = forms.FileField()
    """
