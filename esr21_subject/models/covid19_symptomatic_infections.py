from django.db import models
from edc_base.model_fields import OtherCharField
from edc_base.model_managers import HistoricalRecords
from edc_constants.choices import YES_NO

from .list_models import SymptomaticInfections
from .model_mixins import CrfModelMixin
from ..choices import INFECTION_STATUS


class Covid19SymptomaticInfections(CrfModelMixin):

    symptomatic_experiences = models.CharField(
        verbose_name='Has the participant experienced any symptomatic'
                     ' infection(s)?',
        max_length=20,
        choices=YES_NO, )

    symptomatic_infections = models.ManyToManyField(
        SymptomaticInfections,
        verbose_name='Symptomatic infections ',
        blank=True
    )

    symptomatic_infections_other = OtherCharField()

    date_of_infection = models.DateField(
        verbose_name='Date of symptomatic infection (DD MMM YYYY):',
        null=True,
        blank=True)

    infection_status = models.CharField(
        verbose_name='Previous SARS coV-2 infection status?',
        max_length=20,
        choices=INFECTION_STATUS, )

    hospitalisation_visit = models.CharField(
        verbose_name='Any hospital/ inpatient/ emergency room visit?',
        max_length=20,
        choices=YES_NO, )

    hospitalisation_date = models.DateField(
        verbose_name='Date of hospitalisation:',
        blank=True,
        null=True, )

    history = HistoricalRecords()

    class Meta(CrfModelMixin.Meta):
        app_label = 'esr21_subject'
        verbose_name = 'Covid19 Symptomatic Infections'
        verbose_name_plural = 'Covid19 Symptomatic Infections'
