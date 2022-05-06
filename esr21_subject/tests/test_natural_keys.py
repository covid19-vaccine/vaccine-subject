from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_constants.constants import NO
from edc_facility.import_holidays import import_holidays
from edc_sync.models import OutgoingTransaction
from edc_sync.tests import SyncTestHelper
from model_mommy import mommy

from ..helper_classes import EnrollmentHelper
from ..sync_models import sync_models


@tag('nk1')
class TestNaturalKey(TestCase):

    sync_test_helper = SyncTestHelper()

    def setUp(self):
        import_holidays()

        self.eligibility_confirmation = self.subject_screening = mommy.make_recipe(
            'esr21_subject.eligibilityconfirmation',
            age_in_years=40,
            received_vaccines=NO)

        self.options = {
            'screening_identifier': self.eligibility_confirmation.screening_identifier,
            'consent_datetime': get_utcnow() - relativedelta(days=5),
            'version': '1'}

        self.informed_consent = mommy.make_recipe(
            'esr21_subject.informedconsent',
            **self.options)

        mommy.make_recipe(
            'esr21_subject.screeningeligibility',
            subject_identifier=self.informed_consent.subject_identifier)

        self.appointment_1000 = Appointment.objects.get(
            subject_identifier=self.informed_consent.subject_identifier,
            visit_code='1000')

        self.visit_1000 = mommy.make_recipe(
            'esr21_subject.subjectvisit',
            subject_identifier=self.informed_consent.subject_identifier,
            report_datetime=get_utcnow() - relativedelta(days=5),
            appointment=self.appointment_1000)

    def test_natural_key_attrs(self):
        self.sync_test_helper.sync_test_natural_key_attr('esr21_subject')

    def test_get_by_natural_key_attr(self):
        self.sync_test_helper.sync_test_get_by_natural_key_attr('esr21_subject')
