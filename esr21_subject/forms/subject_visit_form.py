from django import forms
from django.apps import apps as django_apps
from django.core.exceptions import ValidationError
from edc_base.sites import SiteModelFormMixin
from edc_constants.constants import OTHER
from edc_visit_tracking.constants import LOST_VISIT, MISSED_VISIT, UNSCHEDULED
from edc_form_validators import FormValidatorMixin
from edc_visit_tracking.form_validators import VisitFormValidator as BaseVisitFormValidator

from ..models import SubjectVisit


class VisitFormValidator(BaseVisitFormValidator):

    informed_cosent_model = 'esr21_subject.informedconsent'

    def clean(self):
        report_datetime = self.cleaned_data.get('report_datetime')
        if self.instance and not getattr(self.instance, 'id', None):
            self.validate_against_consent_datetime(report_datetime=report_datetime)
        super().clean()

    @property
    def informed_consent_model_cls(self):
        return django_apps.get_model(self.informed_cosent_model)

    @property
    def informed_consent_model_obj(self):
        subject_identifier = self.cleaned_data.get('appointment').subject_identifier
        try:
            consent = self.informed_consent_model_cls.objects.filter(
                subject_identifier=subject_identifier).order_by(
                    '-consent_datetime').first()
        except self.informed_consent_model_cls.DoesNotExist:
            raise ValidationError(
                'Please complete the Informed Consent form before proceeding.')
        else:
            return consent

    def validate_reason_and_info_source(self):

        reason = self.cleaned_data.get('reason')

        if (reason == LOST_VISIT and
                self.cleaned_data.get('info_source') in ['clinic_visit_w_subject',
                                                         'other_contact_w_subject']):
            msg = {'info_source': 'Source of information cannot be other contact with '
                   'participant if participant has been lost to follow up.'}
            self._errors.update(msg)
            raise ValidationError(msg)

    def validate_presence(self):
        pass

    def validate_against_consent_datetime(self, report_datetime=None):
        consent = self.informed_consent_model_obj

        if report_datetime and report_datetime < consent.consent_datetime:
            message = {'report_datetime':
                       'Visit date and time cannot be before the consent date and time'}
            self._errors.update(message)
            raise ValidationError(message)

    def validate_required_fields(self):

        self.required_if(
            MISSED_VISIT,
            field='reason',
            field_required='reason_missed')

        self.required_if(
            UNSCHEDULED,
            field='reason',
            field_required='reason_unscheduled')

        self.required_if(
            OTHER,
            field='info_source',
            field_required='info_source_other')


class SubjectVisitForm (
        SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = VisitFormValidator

    class Meta:
        model = SubjectVisit
        fields = '__all__'
