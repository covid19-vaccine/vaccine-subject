from django import forms

from .form_mixins import SubjectModelFormMixin
from ..models import VaccinationDetails
from esr21_subject_validation.form_validators import VaccineDetailsFormValidator


class VaccinationDetailsForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = VaccineDetailsFormValidator

    class Meta:
        model = VaccinationDetails
        fields = '__all__'
