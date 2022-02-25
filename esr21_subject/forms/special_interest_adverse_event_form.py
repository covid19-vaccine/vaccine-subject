from django import forms
from esr21_subject_validation.form_validators import SpecialInterestAERecordFormValidator

from .form_mixins import SubjectModelFormMixin
from ..models import SpecialInterestAdverseEvent, SpecialInterestAdverseEventRecord


class SpecialInterestAdverseEventForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = SpecialInterestAdverseEvent
        fields = '__all__'


class SpecialInterestAdverseEventRecordForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = SpecialInterestAERecordFormValidator

    ae_number = forms.IntegerField(
        label='AE number',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    def has_changed(self):
        return True

    class Meta:
        model = SpecialInterestAdverseEventRecord
        fields = '__all__'
