from django import forms
from django.apps import apps as django_apps


class ConsentVersionModelModelMixin:

    def get_consent_version(self):
        consent_cls = django_apps.get_model('esr21_subject.informedconsent')
        subject_consents = consent_cls.objects.filter(
            subject_identifier=self.subject_identifier,)
        if subject_consents:
            latest_consent = subject_consents.latest('consent_datetime')
            return latest_consent.version
        else:
            raise forms.ValidationError('Missing Subject Consent form, cannot proceed.')

    def save(self, *args, **kwargs):
        self.consent_version = self.get_consent_version()
        super().save(*args, **kwargs)
