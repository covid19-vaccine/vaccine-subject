from django import forms

from esr21_subject_validation.form_validators import \
    OutcomeInlineFormValidator
from .form_mixins import SubjectModelFormMixin
from ..models import PregOutcome, OutcomeInline


class PregOutcomeForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = PregOutcome
        fields = '__all__'


class OutcomeInlineForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = OutcomeInlineFormValidator

    class Meta:
        model = OutcomeInline
        fields = '__all__'
