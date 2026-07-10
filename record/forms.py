from django import forms
from django.forms import inlineformset_factory
from .models import Diary, StudyRecord, StudyRecordItem


class DiaryForm(forms.ModelForm):
    class Meta:
        model = Diary
        fields = ['date', 'title', 'content', 'image', 'location','favorite']
        widgets = {
             'date': forms.DateInput(attrs={'type': 'date'}),
             "user": forms.HiddenInput()
                  }  

class StudyRecordForm(forms.ModelForm):
    class Meta:
        model = StudyRecord
        fields = ['date','memo', 'favorite']
    
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            "user": forms.HiddenInput()}
            


class StudyRecordItemForm(forms.ModelForm):
    class Meta:
        model = StudyRecordItem
        fields = ['subject', 'study_time']
        widgets = {
            'study_time': forms.NumberInput(attrs={'step': 5, 'min': 0}),
        }


StudyRecordItemFormSet = inlineformset_factory(
    StudyRecord,
    StudyRecordItem,
    form=StudyRecordItemForm,
    extra=3,
    can_delete=True
)
