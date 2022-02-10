from django import forms

from ..models import Covid19Results


class Covid19ResultsForm(forms.ModelForm):

    class Meta:
        model = Covid19Results
        fields = '__all__'
