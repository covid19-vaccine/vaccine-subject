from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from edc_base.model_validators import date_not_future
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.sites import SiteModelMixin
from edc_constants.choices import YES_NO

from ..choices import UNIT_OPTIONS, FREQUENCY, CONCOMITANT_ROUTE
from .model_mixins import CrfModelMixin


class ConcomitantMedication(CrfModelMixin):

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'esr21_subject'
        verbose_name = 'Concomitant Medication'
        verbose_name_plural = 'Concomitant Medication'


class MedicationManager(models.Manager):

    def get_by_natural_key(self, medication_name, administered_date, dose):
        return self.get(medication_name=medication_name,
                        administered_date=administered_date,
                        dose=dose)


class Medication(SiteModelMixin, BaseUuidModel):

    concomitant_medication = models.ForeignKey(
        ConcomitantMedication,
        on_delete=models.PROTECT)

    administered_date = models.DateField(
        verbose_name='Date of administration (DD MMM YYYY):',
        validators=[date_not_future])

    medication_name = models.CharField(
        verbose_name='Name of concomitant medication ',
        max_length=40,
    )

    atc_code = models.CharField(
        verbose_name='ATC code',
        blank=True,
        max_length=30)

    dose = models.DecimalField(
        verbose_name='Dose',
        validators=[MinValueValidator(Decimal('0.00'))],
        decimal_places=2,
        blank=True,
        max_digits=6)  # can only accept positive numbers

    unit = models.CharField(
        verbose_name='Unit',
        max_length=25,
        choices=UNIT_OPTIONS)

    unit_other = models.CharField(
        verbose_name='Other, specify',
        max_length=25,
        blank=True,
        null=True)

    frequency = models.CharField(
        verbose_name='Frequency',
        max_length=25,
        choices=FREQUENCY)

    frequency_other = models.CharField(
        verbose_name='Other, specify',
        max_length=25,
        blank=True,
        null=True)

    route = models.CharField(
        verbose_name='Route',
        max_length=25,
        choices=CONCOMITANT_ROUTE)

    route_other = models.CharField(
        verbose_name='Other, specify',
        max_length=25,
        blank=True,
        null=True)

    reason_of_use = models.TextField(
        verbose_name='Reason for use',)

    ongoing = models.CharField(
        verbose_name='Ongoing',
        max_length=25,
        choices=YES_NO)

    stop_date = models.DateField(
        verbose_name='Stop Date (DD MMM YYYY)',
        validators=[date_not_future, ],
        null=True,
        blank=True)

    prohibited = models.CharField(
        verbose_name='Is concomitant medication prohibited?',
        max_length=25,
        choices=YES_NO)

    reason_prohibited = models.TextField(
        verbose_name='Prohibited medication, further details, i.e.,'
                     'Specify, reason',
        help_text='The use of concomitant medications and/or vaccines,  will '
                  'not definitively require withdrawal of the participant '
                  'from the study, but may determine a '
                  'participant’s eligibility to '
                  'receive a second dose or evaluability in the per-protocol '
                  'analysis set - please refer to the Protocol for further'
                  ' guidance',
        blank=True,
    )

    history = HistoricalRecords()

    objects = MedicationManager()

    def natural_key(self):
        return (self.medication_name, self.administered_date, self.dose, ) + self.concomitant_medication.natural_key()

    natural_key.dependencies = ['esr21_subject.concomitantmedication']

    class Meta:
        app_label = 'esr21_subject'
        unique_together = ('concomitant_medication', 'medication_name',
                           'administered_date', 'dose')
        verbose_name = 'Medication'
        verbose_name_plural = 'Medications'
