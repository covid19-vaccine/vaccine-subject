from django import forms

from .form_mixins import SubjectModelFormMixin
from ..models import PhysicalExam
from esr21_subject_validation.form_validators import PhysicalFormValidator


class PhysicalExamForm(SubjectModelFormMixin, forms.ModelForm):
    form_validator_cls = PhysicalFormValidator

    class Meta:
        model = PhysicalExam
        fields = '__all__'
