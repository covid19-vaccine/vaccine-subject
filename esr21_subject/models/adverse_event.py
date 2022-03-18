from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import date_not_future
from edc_base.sites import SiteModelMixin
from edc_constants.choices import YES_NO
from edc_meddra.model_mixin import MedDRAModelMixin
from edc_protocol.validators import date_not_before_study_start

from ..choices import ACTION_TAKEN, AE_GRADE, TREATMENT_RELATIONSHIP
from ..choices import OUTCOME
from .model_mixins import CrfModelMixin
from esr21_subject.models.informed_consent import InformedConsent


class AdverseEventRecordManager(models.Manager):

    def get_by_natural_key(self, ae_name, start_date, adverse_event):
        return self.get(adverse_event=adverse_event,
                        ae_name=ae_name,
                        start_date=start_date)


class AdverseEvent(CrfModelMixin):
    """"Adverse Event"""""

    experienced_ae = models.CharField(
        verbose_name='Did the participant experience any Adverse Event?',
        choices=YES_NO,
        max_length=3)

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'esr21_subject'
        verbose_name = 'Adverse Event'


class AdverseEventRecord(MedDRAModelMixin, SiteModelMixin, BaseUuidModel):

    adverse_event = models.ForeignKey(
        AdverseEvent,
        on_delete=models.PROTECT,
        max_length=25)

    ae_number = models.PositiveIntegerField(
        verbose_name='AE Number', )

    ae_term = models.CharField(
        verbose_name='AE reported term',
        max_length=100)

    ae_details = models.TextField(
        verbose_name='Details of the AE', )

    start_date = models.DateField(
        verbose_name='AE Start Date',
        validators=[
            date_not_before_study_start,
            date_not_future, ])

    stop_date = models.DateField(
        verbose_name='AE Stop Date',
        validators=[date_not_future, ],
        null=True,
        blank=True)

    substance_hypersensitivity = models.CharField(
        verbose_name=('Any hypersensitivity to the active substance or to any of the '
                      'excipients?'),
        choices=YES_NO,
        max_length=3,
    )

    study_treatmnt_rel = models.CharField(
        verbose_name='Relationship to study treatment',
        max_length=15,
        null=True,
        choices=TREATMENT_RELATIONSHIP)

    nonstudy_treatmnt_rel = models.CharField(
        verbose_name='Relationship to non-study treatment',
        max_length=15,
        null=True,
        choices=TREATMENT_RELATIONSHIP)

    studyproc_treatmnt_rel = models.CharField(
        verbose_name='Relationship to study procedure',
        max_length=15,
        null=True,
        choices=TREATMENT_RELATIONSHIP,
    )

    outcome = models.CharField(
        verbose_name='Outcome',
        max_length=50,
        choices=OUTCOME,
        blank=True,
        null=True)

    sequelae_specify = OtherCharField(
        verbose_name='If recovered / resolved with sequelae, please specify sequelae',
        max_length=100)

    serious_event = models.CharField(
        verbose_name='Was this considered to be a serious adverse event?',
        max_length=3,
        null=True,
        choices=YES_NO)

    investigation_product = models.CharField(
        verbose_name='Investigational Product',
        max_length=20
    )

    action_taken = models.CharField(
        verbose_name='Action Taken, Investigational Product',
        max_length=25,
        null=True,
        blank=True,
        choices=ACTION_TAKEN)

    ctcae_grade = models.CharField(
        verbose_name='CTCAE Grade',
        max_length=25,
        choices=AE_GRADE)

    max_ctcae_grade = models.CharField(
        verbose_name='Maximum CTCAE Grade',
        max_length=25,
        choices=AE_GRADE)

    special_interest_ae = models.CharField(
        verbose_name='Was the event an AE of special interest?',
        max_length=3,
        null=True,
        choices=YES_NO,
        help_text=('(If Yes, check all serious criteria that apply on the '
                   'corresponding SAE form.)'))

    medically_attended_ae = models.CharField(
        verbose_name='Was the event a medically attended AE?',
        max_length=3,
        null=True,
        choices=YES_NO)

    maae_specify = OtherCharField(
        verbose_name='If MAAE, specify',
        max_length=100, )

    hospitalized = models.CharField(
        verbose_name='Was the participant hospitalized?',
        max_length=3,
        null=True,
        choices=YES_NO)

    treatment_given = models.CharField(
        verbose_name='Was treatment given?',
        max_length=3,
        null=True,
        choices=YES_NO)

    treatmnt_given_specify = OtherCharField(
        verbose_name='If yes, specify details')

    ae_study_discontinued = models.CharField(
        verbose_name='Did the AE cause the subject to discontinue from the study?',
        max_length=3,
        null=True,
        choices=YES_NO)

    discontn_dt = models.DateField(
        verbose_name='Date of discontinuation',
        blank=True,
        null=True)

    covid_related_ae = models.CharField(
        verbose_name='Is this a covid-19 related AE?',
        max_length=3,
        null=True,
        choices=YES_NO)

    ae_rel = models.CharField(
        verbose_name='Reasonable possibility AE caused by IP?',
        choices=YES_NO,
        max_length=3,
    )

    pt_name = models.CharField(
        verbose_name='MedDRA preferred term name',
        max_length=200,

    )

    pt_code = models.PositiveIntegerField(
        verbose_name='MedDRA preferred term code',

    )

    llt_code = models.PositiveIntegerField(
        verbose_name=('MedDRA lowest level term code'),
    )

    llt_name = models.CharField(
        verbose_name=('MedDRA lowest level term name'),
        max_length=200,
    )

    hlt_code = models.PositiveIntegerField(
        verbose_name='MedDRA high level term code',
    )

    hlt_name = models.CharField(
        verbose_name='MedDRA high level term name',
        max_length=200,
    )

    hlgt_code = models.PositiveIntegerField(
        verbose_name='MedDRA high level group term code',
    )

    hlgt_name = models.CharField(
        verbose_name='MedDRA high level group term name',
        max_length=200,
    )

    soc_code = models.PositiveIntegerField(
        verbose_name='MedDRA system organ class code',
    )

    soc_name = models.CharField(
        verbose_name='MedDRA system organ class name',
        max_length=200,
    )

    meddra_v = models.CharField(
        verbose_name='MedDRA version',
        max_length=5,
    )

    ctcae_v = models.CharField(
        verbose_name='CTCAE version',
        max_length=5,
    )

    objects = AdverseEventRecordManager()

    @property
    def dob(self):
        consent = InformedConsent.objects.filter(
            subject_identifier=self.adverse_event.subject_visit.subject_identifier).last()
        return consent.dob

    @property
    def gender(self):
        consent = InformedConsent.objects.filter(
            subject_identifier=self.adverse_event.subject_visit.subject_identifier).last()
        return consent.gender

    history = HistoricalRecords()

    @property
    def update_ae_number(self):
        """Update AE number.
        """
        ae_number = 0
        ae_record_cls = self._meta.model
        ae = ae_record_cls.objects.filter(
            adverse_event=self.adverse_event).order_by('created')
        if ae:
            last_ae = ae.last()
            ae_number = last_ae.ae_number + 1
        else:
            ae_number += 1
        return ae_number

    def natural_key(self):
        return (self.ae_name, self.start_date,) + self.adverse_event.natural_key()

    natural_key.dependencies = ['esr21_subject.adverseevent']

    def save(self, *args, **kwargs):
        if not self.id:
            self.ae_number = self.update_ae_number
        super().save(*args, **kwargs)

    class Meta(CrfModelMixin.Meta):
        verbose_name = 'Adverse Event Record'
        app_label = 'esr21_subject'
