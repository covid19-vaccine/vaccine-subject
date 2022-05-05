from django import forms
from esr21_subject_validation.form_validators import ConcomitantMedicationFormValidator
from .form_mixins import SubjectModelFormMixin
from ..models import ConcomitantMedication, Medication


class ConcomitantMedicationForm(SubjectModelFormMixin, forms.ModelForm):

    class Meta:
        model = ConcomitantMedication
        fields = '__all__'


class MedicationForm(SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = ConcomitantMedicationFormValidator

    def has_changed(self):
        return True

    class Meta:
        model = Medication
        fields = '__all__'
