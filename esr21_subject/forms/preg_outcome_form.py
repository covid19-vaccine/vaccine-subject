from django import forms
from django.core.exceptions import ValidationError

from esr21_subject_validation.form_validators import OutcomeInlineFormValidator
from .form_mixins import SubjectModelFormMixin
from ..models import PregOutcome, OutcomeInline


class PregOutcomeForm(SubjectModelFormMixin, forms.ModelForm):

    def clean(self):
        super().clean()

        total_inlines = self.data.get('outcomeinline_set-TOTAL_FORMS')
        preg_outcome_count = self.cleaned_data.get('outcome_count')

        if preg_outcome_count != int(total_inlines) and preg_outcome_count:
            msg = {
                'outcome_count':
                    'The number of outcomes should match number of inlines'
            }
            raise ValidationError(msg)

        if total_inlines == 0:
            msg = {'outcome_count': 'The complete the outcome inline form'}
            raise ValidationError(msg)

    class Meta:
        model = PregOutcome
        fields = '__all__'


class OutcomeInlineForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = OutcomeInlineFormValidator

    class Meta:
        model = OutcomeInline
        fields = '__all__'
