from django import forms
from edc_base.sites import SiteModelFormMixin
from edc_consent.site_consents import site_consents, SiteConsentError
from edc_consent.exceptions import ConsentObjectDoesNotExist
from edc_consent.modelform_mixins import ConsentModelFormMixin
from edc_form_validators import FormValidatorMixin
from esr21_subject_validation.form_validators import InformedConsentFormValidator
from ..models import InformedConsent


class InformedConsentForm(SiteModelFormMixin, FormValidatorMixin,
                          ConsentModelFormMixin,
                          forms.ModelForm):

    form_validator_cls = InformedConsentFormValidator

    screening_identifier = forms.CharField(
        label='Screening Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    subject_identifier = forms.CharField(
        label='Subject Identifier',
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False)

    def clean_guardian_and_dob(self):
        pass

    @property
    def consent_config(self):
        cleaned_data = self.cleaned_data
        try:
            consent_config = site_consents.get_consent(
                model=self._meta.model._meta.label_lower,
                report_datetime=cleaned_data.get(
                    'consent_datetime') or self.instance.consent_datetime,
                consent_model=self._meta.model._meta.label_lower,
                consent_group=self._meta.model._meta.consent_group,
                version=cleaned_data.get('version') or '3'
            )
        except (ConsentObjectDoesNotExist, SiteConsentError) as e:
            raise forms.ValidationError(e)
        return consent_config

    def update_consent(self):
        consent_datetime = self.cleaned_data.get(
            'consent_datetime') or self.instance.consent_datetime
        if consent_datetime:
            options = dict(
                model=self._meta.model._meta.label_lower,
                consent_model=self._meta.model._meta.label_lower,
                consent_group=self._meta.model._meta.consent_group,
                report_datetime=consent_datetime,
                version=self.cleaned_data.get('version') or '3')
            consent = site_consents.get_consent(**options)
            if consent.updates_versions:
                ConsentHelper(
                    model_cls=self._meta.model,
                    update_previous=False,
                    **self.cleaned_data)

    class Meta:
        model = InformedConsent
        fields = '__all__'
