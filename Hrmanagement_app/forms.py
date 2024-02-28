from django import forms
from django.forms import Form
from django.core.exceptions import ObjectDoesNotExist
from Hrmanagement_app.models import Department, ContractYearModel


class DateInput(forms.DateInput):
    input_type = "date"


class AddStaffForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Password", max_length=50,
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    phone = forms.CharField(label="Phone", max_length=12, widget=forms.NumberInput(attrs={"class": "form-control"}))
    i_d = forms.CharField(label="National_ID", max_length=10, widget=forms.NumberInput(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            departments = Department.objects.all()
            self.fields['department_id'] = forms.ChoiceField(label="Department",
                                                             choices=[(department.id, department.department_name) for
                                                                      department in departments],
                                                             widget=forms.Select(attrs={"class": "form-control"}))
        except ObjectDoesNotExist:
            self.fields['department_id'] = forms.ChoiceField(label="Department", choices=[],
                                                             widget=forms.Select(attrs={"class": "form-control"}))

        try:
            contract_years = ContractYearModel.objects.all()
            self.fields['contract_year_id'] = forms.ChoiceField(label="Contract Year", choices=[
                (contract_year.id, f"{contract_year.contract_start_year} to {contract_year.contract_end_year}") for
                contract_year in contract_years], widget=forms.Select(attrs={"class": "form-control"}))
        except ObjectDoesNotExist:
            self.fields['contract_year_id'] = forms.ChoiceField(label="Contract Year", choices=[],
                                                                widget=forms.Select(attrs={"class": "form-control"}))

    gender_list = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    gender = forms.ChoiceField(label="Gender", choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))


class EditStaffForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=50, widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(label="First Name", max_length=50,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(label="Last Name", max_length=50,
                                widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(label="Username", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Address", max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    phone = forms.CharField(label="Phone", max_length=12, widget=forms.NumberInput(attrs={"class": "form-control"}))
    i_d = forms.CharField(label="National_ID", max_length=10, widget=forms.NumberInput(attrs={"class": "form-control"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            departments = Department.objects.all()
            self.fields['department_id'] = forms.ChoiceField(label="Department",
                                                             choices=[(department.id, department.department_name) for
                                                                      department in departments],
                                                             widget=forms.Select(attrs={"class": "form-control"}))
        except ObjectDoesNotExist:
            self.fields['department_id'] = forms.ChoiceField(label="Department", choices=[],
                                                             widget=forms.Select(attrs={"class": "form-control"}))

        try:
            contract_years = ContractYearModel.objects.all()
            self.fields['contract_year_id'] = forms.ChoiceField(label="Contract Year", choices=[
                (contract_year.id, f"{contract_year.contract_start_year} to {contract_year.contract_end_year}") for
                contract_year in contract_years], widget=forms.Select(attrs={"class": "form-control"}))
        except ObjectDoesNotExist:
            self.fields['contract_year_id'] = forms.ChoiceField(label="Contract Year", choices=[],
                                                                widget=forms.Select(attrs={"class": "form-control"}))

    gender_list = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    gender = forms.ChoiceField(label="Gender", choices=gender_list,
                               widget=forms.Select(attrs={"class": "form-control"}))
    profile_pic = forms.FileField(label="Profile Pic", required=False,
                                  widget=forms.FileInput(attrs={"class": "form-control"}))
