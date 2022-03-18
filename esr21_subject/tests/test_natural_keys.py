from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_constants.constants import NO, FEMALE, OMANG
from edc_facility.import_holidays import import_holidays
from edc_sync.tests import SyncTestHelper
from model_mommy import mommy
from edc_visit_tracking.constants import SCHEDULED
from edc_visit_schedule.site_visit_schedules import site_visit_schedules
from ..models import ScreeningEligibility



@tag('nk1')
class TestNaturalKey(TestCase):

    sync_test_helper = SyncTestHelper()

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
            cohort = 'esr21'
            onschedule_model = 'esr21_subject.onschedule'

            self.put_on_schedule(f'{cohort}_enrol_schedule', onschedule_model=onschedule_model,
                                 onschedule_datetime=screening_eligibility.created.replace(microsecond=0))

            self.put_on_schedule(f'{cohort}_fu_schedule',
                                 onschedule_model=onschedule_model,
                                 onschedule_datetime=screening_eligibility.created.replace(microsecond=0))

            self.subject_visit = mommy.make_recipe(
                'esr21_subject.subjectvisit',
                appointment=Appointment.objects.get(
                    visit_code='1000',
                    subject_identifier=self.subject_consent.subject_identifier),
                report_datetime=get_utcnow(),
                reason=SCHEDULED)

        self.appointment_1000 = Appointment.objects.get(
            subject_identifier=self.subject_consent.subject_identifier,
            visit_code='1000')

        self.visit_1000 = mommy.make_recipe(
            'esr21_subject.subjectvisit',
            subject_identifier=self.subject_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=5),
            appointment=self.appointment_1000)

    def test_natural_key_attrs(self):
        #self.sync_test_helper.sync_test_natural_key_attr('esr21_subject')
        pass

    def test_get_by_natural_key_attr(self):
        #self.sync_test_helper.sync_test_get_by_natural_key_attr('esr21_subject')
        pass

    def put_on_schedule(self, schedule_name, onschedule_model, onschedule_datetime=None):
        _, schedule = site_visit_schedules.get_by_onschedule_model_schedule_name(
            onschedule_model=onschedule_model, name=schedule_name)
        schedule.put_on_schedule(
            subject_identifier=self.subject_identifier,
            onschedule_datetime=onschedule_datetime,
            schedule_name=schedule_name)
