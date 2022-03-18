from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_constants.constants import OMANG, FEMALE, MALE, NO, YES, NEG
from edc_facility.import_holidays import import_holidays
from edc_metadata.constants import REQUIRED, NOT_REQUIRED
from edc_metadata.models import CrfMetadata, RequisitionMetadata
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy

from ..models import ScreeningEligibility, Covid19Results


@tag('rg')
class TestRuleGroups(TestCase):

    def setUp(self):
        import_holidays()

        self.eligibility = mommy.make_recipe(
            'esr21_subject.eligibilityconfirmation')

        self.consent_options = {
            'screening_identifier': self.eligibility.screening_identifier,
            'consent_datetime': get_utcnow(),
            'version': 1,
            'dob': (get_utcnow() - relativedelta(years=45)).date(),
            'first_name': 'TEST ONE',
            'last_name': 'TEST',
            'initials': 'TOT',
            'identity': '123425678',
            'confirm_identity': '123425678',
            'identity_type': OMANG,
            'gender': FEMALE}

        self.subject_consent = mommy.make_recipe(
            'esr21_subject.informedconsent',
            **self.consent_options)

        mommy.make_recipe(
            'esr21_subject.screeningeligibility',
            subject_identifier=self.subject_consent.subject_identifier)

        self.subject_identifier = self.subject_consent.subject_identifier

        screening_eligibility = ScreeningEligibility.objects.get(
            subject_identifier=self.subject_identifier)

        if screening_eligibility.is_eligible:
            self.put_subject_on_schedule(created=screening_eligibility.created,
                                         subject_identifier=self.subject_identifier)
            self.subject_visit = mommy.make_recipe(
                'esr21_subject.subjectvisit',
                appointment=Appointment.objects.get(
                    visit_code='1000',
                    subject_identifier=self.subject_consent.subject_identifier),
                report_datetime=get_utcnow(),
                reason=SCHEDULED)

    @tag('rg1')
    def test_pregnancy_form_required(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.pregnancystatus',
                subject_identifier=self.subject_identifier,
                visit_code='1000',
                visit_code_sequence='0').entry_status, REQUIRED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.pregnancytest',
                subject_identifier=self.subject_identifier,
                visit_code='1000',
                visit_code_sequence='0').entry_status, NOT_REQUIRED)

    def test_pregnancy_status_form_not_required(self):

        eligibility = mommy.make_recipe(
            'esr21_subject.eligibilityconfirmation')

        consent_options = {
            'screening_identifier': eligibility.screening_identifier,
            'consent_datetime': get_utcnow(),
            'version': 1,
            'dob': (get_utcnow() - relativedelta(years=45)).date(),
            'first_name': 'JOHN',
            'last_name': 'DOE',
            'initials': 'JD',
            'identity': '123415678',
            'confirm_identity': '123415678',
            'identity_type': OMANG,
            'gender': MALE}

        subject_consent = mommy.make_recipe(
            'esr21_subject.informedconsent',
            **consent_options)

        self.put_subject_on_schedule(created=subject_consent.created,
                                     subject_identifier=subject_consent.subject_identifier)

        mommy.make_recipe(
            'esr21_subject.screeningeligibility',
            subject_identifier=subject_consent.subject_identifier)

        mommy.make_recipe(
            'esr21_subject.subjectvisit',
            appointment=Appointment.objects.get(
                visit_code='1000',
                subject_identifier=subject_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.pregnancystatus',
                subject_identifier=subject_consent.subject_identifier,
                visit_code='1000',
                visit_code_sequence='0').entry_status, NOT_REQUIRED)

    def test_pregnancy_test_not_required(self):
        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.pregnancytest',
                subject_identifier=self.subject_identifier,
                visit_code='1000',
                visit_code_sequence='0').entry_status, NOT_REQUIRED)

    @tag('pt1')
    def test_pregnancy_test_required(self):
        self.consent_options['dob'] = (get_utcnow() - relativedelta(years=55)).date()
        self.consent_options['identity'] = '111125678'
        self.consent_options['confirm_identity'] = '111125678'

        subject_consent = mommy.make_recipe(
            'esr21_subject.informedconsent',
            **self.consent_options)

        self.put_subject_on_schedule(created=subject_consent.created,
                                     subject_identifier=subject_consent.subject_identifier)

        mommy.make_recipe(
            'esr21_subject.screeningeligibility',
            subject_identifier=subject_consent.subject_identifier)

        subject_visit = mommy.make_recipe(
            'esr21_subject.subjectvisit',
            appointment=Appointment.objects.get(
                visit_code='1000',
                subject_identifier=subject_consent.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'esr21_subject.pregnancystatus',
            subject_visit=subject_visit,
            post_menopausal=NO,
            surgically_sterilized=NO)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.pregnancytest',
                subject_identifier=subject_consent.subject_identifier,
                visit_code='1000',
                visit_code_sequence='0').entry_status, REQUIRED)

    @tag('cr')
    def test_covid19_results(self):
        #
        # appointment = Appointment.objects.get(
        #         visit_code='1000',
        #         subject_identifier=self.subject_identifier)
        #
        # subject_visit = mommy.make_recipe(
        #     'esr21_subject.subjectvisit',
        #     appointment=appointment,
        #     report_datetime=get_utcnow(),
        #     reason=SCHEDULED)

        mommy.make_recipe(
            'esr21_subject.covid19results',
            subject_visit=self.subject_visit,
            covid_result=NEG)

        covid19 = CrfMetadata.objects.filter(subject_identifier=self.subject_identifier)

        self.assertEqual(
            CrfMetadata.objects.get(
                model='esr21_subject.physicalexam',
                subject_identifier=self.subject_identifier,
                visit_code='1000',
                visit_code_sequence='0').entry_status, REQUIRED)

    def put_subject_on_schedule(self, created, subject_identifier):
        cohort = 'esr21'
        onschedule_model = 'esr21_subject.onschedule'

        self.put_on_schedule(f'{cohort}_enrol_schedule',
                             onschedule_model=onschedule_model,
                             onschedule_datetime=created.replace(microsecond=0),
                             subject_identifier=subject_identifier)

        self.put_on_schedule(f'{cohort}_fu_schedule',
                             onschedule_model=onschedule_model,
                             onschedule_datetime=created.replace(microsecond=0),
                             subject_identifier=subject_identifier)

    def put_on_schedule(self, schedule_name, onschedule_model,
                        onschedule_datetime=None, subject_identifier=None):
        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=onschedule_model, name=schedule_name)
        schedule.put_on_schedule(
            subject_identifier=subject_identifier,
            onschedule_datetime=onschedule_datetime,
            schedule_name=schedule_name)
