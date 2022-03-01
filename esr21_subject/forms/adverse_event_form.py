from django import forms
from django.apps import apps as django_apps
from edc_constants.constants import YES, NO
from edc_meddra.form_mixin import MedDRAFormMixin
from esr21_subject_validation.form_validators import AdverseEventRecordFormValidator


from ..models import AdverseEvent, AdverseEventRecord
from .form_mixins import SubjectModelFormMixin


class AdverseEventForm(SubjectModelFormMixin, forms.ModelForm):

    ae_record = 'esr21_subject.adverseeventrecord'

    @property
    def ae_record_cls(self):
        return django_apps.get_model(self.ae_record)

    def clean(self):
        experienced_ae = self.data.get('experienced_ae')
        ae_count = int(self.data.get('adverseeventrecord_set-TOTAL_FORMS'))
        if experienced_ae == YES and ae_count == 0:
            msg = ('Participant has experienced an adverse event, '
                   f'{self.ae_record_cls._meta.verbose_name} is required')
            raise forms.ValidationError(msg)

    class Meta:
        model = AdverseEvent
        fields = '__all__'


class AdverseEventRecordForm(MedDRAFormMixin, SubjectModelFormMixin, forms.ModelForm):

    form_validator_cls = AdverseEventRecordFormValidator

    ae_number = forms.IntegerField(
        label='AE number',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    def __init__(self, *args, **kwargs):
        version = django_apps.get_app_config('edc_meddra').version
        ctcae_version = django_apps.get_app_config('edc_meddra').ctcae_version
        initial = kwargs.pop('initial', {})
        initial['meddra_v'] = initial.get('meddra_v', version)
        initial['ctcae_v'] = initial.get('ctcae_v', ctcae_version)
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(AdverseEventRecordForm, self).clean()
        serious_event = cleaned_data.get('serious_event')
        serious_ae = self.data.get('seriousadverseevent_set-TOTAL_FORMS')

        if serious_event and serious_ae:
            """
            Null exception fix
            """
            if serious_event == YES and int(serious_ae) == 0:
                msg = {'serious_event':
                       'Please complete the serious adverse event table.'}
                raise forms.ValidationError(msg)
            elif serious_event == NO and int(serious_ae) != 0:
                msg = {'serious_event':
                       'This is not a serious AE, please *DO NOT* complete the'
                       ' serious adverse event table.'}
                raise forms.ValidationError(msg)

        special_interest_ae = cleaned_data.get('special_interest_ae')
        aesi = self.data.get('specialinterestadverseevent_set-TOTAL_FORMS')

        if special_interest_ae and aesi:
            """
            Null exception fix
            """
            if special_interest_ae == YES and aesi and int(aesi) == 0:
                msg = {'special_interest_ae':
                       'Please complete the AEs of special interest table.'}
                raise forms.ValidationError(msg)
            elif special_interest_ae == NO and int(aesi) != 0:
                msg = {'special_interest_ae':
                       'This is not an AE of special interest, please *DO NOT* '
                       'complete the AEs of special interest table.'}
                raise forms.ValidationError(msg)

    class Meta:
        model = AdverseEventRecord
        fields = '__all__'
