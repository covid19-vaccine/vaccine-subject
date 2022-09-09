from django.apps import apps as django_apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    
    help = 'Create or Update the ScreenOut objects'
    
    screening_eligibility_model = 'esr21_subject.screeningeligibility'
    vaccination_details_model = 'esr21_subject.vaccinationdetails'
    informed_consent_model = 'esr21_subject.informedconsent'
    screen_out = 'esr21_subject.screenout'
    
    @property
    def vaccination_details_cls(self):
        return django_apps.get_model(self.vaccination_details_model)
    
    @property
    def screening_eligibility_cls(self):
        return django_apps.get_model(self.screening_eligibility_model)
    
    @property
    def screening_out_cls(self):
        return django_apps.get_model(self.screen_out)

    @property
    def consent_model_cls(self):
        return django_apps.get_model(self.informed_consent_model)
    
    def generate_screen_out(self):
        consent_idx = self.consent_model_cls.objects.all().values_list('subject_identifier', flat=True)
        for idx in consent_idx:
            try:
                obj = self.screening_eligibility_cls.objects.get(
                    subject_identifier=idx)
            except self.screening_eligibility_cls.DoesNotExist:
                pass
            else:
                if obj.is_eligible:
                    vac_details = self.vaccination_details_cls.objects.filter(
                        subject_visit__subject_identifier=idx,
                        received_dose='YES')
                    if vac_details.count() == 0:
                        options = {
                            'screen_out_reason':'',
                            'screen_out_other':'',
                            'comment':'',
                        }
                        self.screening_out_cls.objects.update_or_create(subject_identifier=idx, **options)   
    