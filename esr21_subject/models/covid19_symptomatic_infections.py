from django.db import models

from edc_constants.choices import YES_NO
from .model_mixins import CrfModelMixin
from ..choices import INFECTION_STATUS


class Covid19SymptomaticInfections(CrfModelMixin):
    symptomatic_experiences = models.CharField(
        verbose_name='Has the participant experienced any symptomatic'
                     ' infection(s)?',
        max_length=20,
        choices=YES_NO, )

    date_of_infection = models.DateField(
        verbose_name='Date of symptomatic infection:')

    infection_status = models.CharField(
        verbose_name='Previous SARS coV-2 infection status?',
        max_length=20,
        choices=INFECTION_STATUS, )

    visits = models.CharField(
        verbose_name='Any hospital/ inpatient/ emergency room visit?',
        max_length=20,
        choices=YES_NO, )

    hospitalisation_date = models.DateField(
        verbose_name='Date of hospitalisation:')

    hospitalisation_details = models.TextField(
        verbose_name='Date of hospitalisation:',
        max_length=150,
        blank=True,
        null=True)

    class Meta(CrfModelMixin.Meta):
        app_label = 'esr21_subject'
        verbose_name = 'Covid19 Symptomatic Infections'
        verbose_name_plural = 'Covid19 Symptomatic Infections'
