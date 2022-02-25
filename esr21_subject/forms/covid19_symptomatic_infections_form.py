from django import forms

from .form_mixins import SubjectModelFormMixin
from ..models import Covid19SymptomaticInfections
from esr21_subject_validation.form_validators import \
    Covid19SymptomaticInfectionsFormValidator


class Covid19SymptomaticInfectionsForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = Covid19SymptomaticInfectionsFormValidator

    class Meta:
        model = Covid19SymptomaticInfections
        fields = '__all__'
