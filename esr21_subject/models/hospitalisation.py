from django.db import models
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO

from ..choices import (HOSPITALISATION_STATUS,
                       HOSPITALISATION_REASON, HOSPITALISATION_OUTCOME)
from .model_mixins import CrfModelMixin
from .list_models import COVIDSymptoms


class Hospitalisation(CrfModelMixin):
    status = models.CharField(
        verbose_name='Hospitalisation Status',
        max_length=50,
        choices=HOSPITALISATION_STATUS)

    start_date = models.DateField(
        verbose_name='Start date of hospitalisation')

    stop_date = models.DateField(
        verbose_name='Stop date of hospitalisation',
        null=True,
        blank=True)

    ongoing = models.CharField(
        max_length=3,
        choices=YES_NO)

    reason = models.CharField(
        verbose_name='Primary reason for hospital/ inpatient/ ER visit',
        max_length=50,
        choices=HOSPITALISATION_REASON, )

    reason_other = OtherCharField(
        verbose_name='If Other, specify',
        max_length=100,
        null=True,
        blank=True,
    )

    covid_symptoms = models.ManyToManyField(
        COVIDSymptoms,
        verbose_name=('If COVID-19 related symptoms, please check all that '
                      'apply'),
        blank=True)

    hospitalisation_outcome = models.CharField(
        verbose_name='Hospitalisation Outcome',
        max_length=90,
        choices=HOSPITALISATION_OUTCOME,
        null=True,
        blank=True
    )

    class Meta(CrfModelMixin.Meta):
        app_label = 'esr21_subject'
        verbose_name = 'Hospitalisation'
        verbose_name_plural = 'Hospitalisation'
