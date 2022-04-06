from django.test import TestCase, tag
from edc_appointment.models import Appointment
from edc_base.utils import get_utcnow
from edc_constants.constants import YES
from edc_facility.import_holidays import import_holidays
from edc_visit_tracking.constants import SCHEDULED
from model_mommy import mommy
from ..models import OnSchedule, OnScheduleIll
from edc_appointment.constants import COMPLETE_APPT
from edc_visit_schedule.site_visit_schedules import site_visit_schedules


@tag('vs')
class TestVisitScheduleSetup(TestCase):

    databases = '__all__'

    def setUp(self):
        import_holidays()

    @tag('vsm')
    def test_consented_onschedule_maincohort(self):
        """Assert that a participant is put onschedule for main study.
        """

        mommy.make_recipe(
            'esr21_subject.eligibilityconfirmation',)

        consent = mommy.make_recipe(
            'esr21_subject.informedconsent',
            subject_identifier='123-9876')

        self.put_subject_on_schedule(consent.created,
                                     consent.subject_identifier)

        screening_eligibility = mommy.make_recipe(
            'esr21_subject.screeningeligibility',
            subject_identifier=consent.subject_identifier,
            is_eligible=True)

        self.assertEqual(OnSchedule.objects.filter(
            subject_identifier=screening_eligibility.subject_identifier,
            schedule_name='esr21_enrol_schedule').count(), 1)

        self.assertEqual(OnSchedule.objects.filter(
            subject_identifier=screening_eligibility.subject_identifier,
            schedule_name='esr21_fu_schedule').count(), 1)

    # @tag('vs0')
    # def test_consented_onschedule_subcohort(self):
        # """Assert that a participant is put onschedule for subcohort.
        # """
        # for i in range(3001):
            # mommy.make_recipe(
                # 'esr21_subject.eligibilityconfirmation',)
                #
            # mommy.make_recipe(
                # 'esr21_subject.informedconsent',
                # subject_identifier=f'123-987{i}')
                #
        # self.assertEqual(OnSchedule.objects.filter(
            # subject_identifier='123-9873000',
            # schedule_name='esr21_sub_enrol_schedule').count(), 1)
            #
        # self.assertEqual(OnSchedule.objects.filter(
            # subject_identifier='123-9873000',
            # schedule_name='esr21_sub_fu_schedule').count(), 1)

    @tag('vs1')
    def test_illness_onschedule(self):
        """Assert that a participant is put onschedule for illness visits if
         they test positive for Covid 19.
        """

        mommy.make_recipe(
            'esr21_subject.eligibilityconfirmation')

        consent = mommy.make_recipe(
            'esr21_subject.informedconsent',
            subject_identifier='123-9877')

        self.put_subject_on_schedule(consent.created,
                                     consent.subject_identifier)

        screening_eligibility = mommy.make_recipe(
            'esr21_subject.screeningeligibility',
            subject_identifier=consent.subject_identifier,
            is_eligible=True)

        mommy.make_recipe(
            'esr21_subject.subjectvisit',
            appointment=Appointment.objects.get(visit_code='1000'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        visit = mommy.make_recipe(
            'esr21_subject.subjectvisit',
            appointment=Appointment.objects.get(visit_code='1007'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'esr21_subject.covid19symptomaticinfections',
            subject_visit=visit,
            symptomatic_experiences=YES)

        self.assertEqual(OnScheduleIll.objects.filter(
            subject_identifier=screening_eligibility.subject_identifier,
            schedule_name='esr21_illness_schedule').count(), 1)

    @tag('vs2')
    def test_illness_not_onschedule(self):
        """Assert that a participant is not put onschedule for illness visits if
         they test positive for Covid 19 and they are already on an illness schedule.
        """

        mommy.make_recipe(
            'esr21_subject.eligibilityconfirmation',)

        consent = mommy.make_recipe(
            'esr21_subject.informedconsent',
            subject_identifier='123-9877')

        self.put_subject_on_schedule(consent.created,
                                     consent.subject_identifier)

        screening_eligibility = mommy.make_recipe(
            'esr21_subject.screeningeligibility',
            subject_identifier=consent.subject_identifier,
            is_eligible=True)

        mommy.make_recipe(
            'esr21_subject.subjectvisit',
            appointment=Appointment.objects.get(visit_code='1000'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        visit1 = mommy.make_recipe(
            'esr21_subject.subjectvisit',
            appointment=Appointment.objects.get(visit_code='1007'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'esr21_subject.covid19symptomaticinfections',
            subject_visit=visit1,
            symptomatic_experiences=YES)

        self.assertEqual(OnScheduleIll.objects.filter(
            subject_identifier=screening_eligibility.subject_identifier,
            schedule_name='esr21_illness_schedule').count(), 1)

        visit2 = mommy.make_recipe(
            'esr21_subject.subjectvisit',
            appointment=Appointment.objects.get(visit_code='1014'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'esr21_subject.covid19symptomaticinfections',
            subject_visit=visit2,
            symptomatic_experiences=YES)

        self.assertEqual(OnScheduleIll.objects.filter(
            subject_identifier=screening_eligibility.subject_identifier,
            schedule_name='esr21_illness1_schedule').count(), 0)

    @tag('vs3')
    def test_illness2_onschedule(self):
        """Assert that a participant is put onschedule for second illness visits if
         they test positive for Covid 19 for the second time.
        """

        mommy.make_recipe(
            'esr21_subject.eligibilityconfirmation',)

        consent = mommy.make_recipe(
            'esr21_subject.informedconsent',
            subject_identifier='123-9877')

        screening_eligibility = mommy.make_recipe(
            'esr21_subject.screeningeligibility',
            subject_identifier=consent.subject_identifier,
            is_eligible=True)

        self.put_subject_on_schedule(consent.created,
                                     consent.subject_identifier)

        mommy.make_recipe(
            'esr21_subject.subjectvisit',
            appointment=Appointment.objects.get(
                visit_code='1000',
                subject_identifier=screening_eligibility.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        visit1 = mommy.make_recipe(
            'esr21_subject.subjectvisit',
            appointment=Appointment.objects.get(
                visit_code='1007',
                subject_identifier=screening_eligibility.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'esr21_subject.covid19symptomaticinfections',
            subject_visit=visit1,
            symptomatic_experiences=YES)

        self.assertEqual(OnScheduleIll.objects.filter(
            subject_identifier=screening_eligibility.subject_identifier,
            schedule_name='esr21_illness_schedule').count(), 1)

        appt = Appointment.objects.get(
                visit_code='2028',
                subject_identifier=screening_eligibility.subject_identifier)

        appt.appt_status = COMPLETE_APPT
        appt.save()

        # mommy.make_recipe(
            # 'esr21_subject.offscheduleill',
            # subject_identifier=informed_consent.subject_identifier)

        visit2 = mommy.make_recipe(
            'esr21_subject.subjectvisit',
            appointment=Appointment.objects.get(visit_code='1014'),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'esr21_subject.covid19symptomaticinfections',
            subject_visit=visit2,
            symptomatic_experiences=YES)

        self.assertEqual(OnScheduleIll.objects.filter(
            subject_identifier=screening_eligibility.subject_identifier,
            schedule_name='esr21_illness2_schedule').count(), 1)

    @tag('vs3')
    def test_illness2_onschedule_invalid(self):
        """Assert that a participant is not put onschedule for second illness visit
        """

        mommy.make_recipe(
            'esr21_subject.eligibilityconfirmation',)

        consent = mommy.make_recipe(
            'esr21_subject.informedconsent',
            subject_identifier='123-9877')

        screening_eligibility = mommy.make_recipe(
            'esr21_subject.screeningeligibility',
            subject_identifier=consent.subject_identifier,
            is_eligible=True)

        self.put_subject_on_schedule(consent.created,
                                     consent.subject_identifier)

        mommy.make_recipe(
            'esr21_subject.subjectvisit',
            appointment=Appointment.objects.get(
                visit_code='1000',
                subject_identifier=screening_eligibility.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        visit1 = mommy.make_recipe(
            'esr21_subject.subjectvisit',
            appointment=Appointment.objects.get(
                visit_code='1007',
                subject_identifier=screening_eligibility.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'esr21_subject.covid19symptomaticinfections',
            subject_visit=visit1,
            symptomatic_experiences=YES)

        visit2 = mommy.make_recipe(
            'esr21_subject.subjectvisit',
            appointment=Appointment.objects.get(
                visit_code='1014',
                subject_identifier=screening_eligibility.subject_identifier),
            report_datetime=get_utcnow(),
            reason=SCHEDULED)

        mommy.make_recipe(
            'esr21_subject.covid19symptomaticinfections',
            subject_visit=visit2,
            symptomatic_experiences=YES)

        self.assertEqual(OnScheduleIll.objects.filter(
            subject_identifier=screening_eligibility.subject_identifier,
            schedule_name='esr21_illness_schedule').count(), 1)

        self.assertNotEqual(OnScheduleIll.objects.filter(
            subject_identifier=screening_eligibility.subject_identifier,
            schedule_name='esr21_illness2_schedule').count(), 1)

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
