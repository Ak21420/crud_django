from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ('fullname','mobile','emp_code','position','is_delete')
        labels = {
            'fullname':'Full Name',
            'emp_code':'EMP. Code',
            'is_delete':'Delete'
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeForm,self).__init__(*args, **kwargs)
        self.fields['position'].empty_label = "Select"
        self.fields['emp_code'].required = False
