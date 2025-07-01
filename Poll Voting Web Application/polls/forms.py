from django import forms
from .models import Poll,PollOption

class PollForm(forms.ModelForm):
    close_time = forms.DateTimeField(
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type':"datetime-local"
            }
        ),
        initial='2025-06-30'
    )

    class Meta:
        model = Poll
        fields = ['question', 'close_time']

# this is used for editing the poll option in the form 
class PollOptionForm(forms.ModelForm):
    class Meta:
        model = PollOption
        fields = ['text']

# this is used for adding the poll option in the form 
class OptionForm(forms.Form):
    option1 = forms.CharField(label='Option 1', max_length=200)
    option2 = forms.CharField(label='Option 2', max_length=200)
    option3 = forms.CharField(label='Option 3 (optional)', max_length=200, required=False)
    option4 = forms.CharField(label='Option 4 (optional)', max_length=200, required=False)