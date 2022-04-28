from django.db import models
from django_countries.fields import CountryField
from edc_base.model_fields import OtherCharField
from edc_constants.choices import YES_NO

from ..maternal_choices import ETHNICITY, HIGHEST_EDUCATION
from .model_mixins import CrfModelMixin
from ..choices import EMPLOYMENT_STATUS, SETTLEMENT_TYPE, MARITAL_STATUS


class DemographicsData(CrfModelMixin):

    # age_at_entry = models.IntegerField(
    #     #     verbose_name='Age at study entry',)

    country = CountryField()

    ethnicity = models.CharField(
        max_length=25,
        verbose_name='Ethnicity ',
        choices=ETHNICITY)

    ethnicity_other = OtherCharField(
        max_length=35,
        verbose_name='If other specify...',
        blank=True,
        null=True,)

    household_members = models.PositiveSmallIntegerField(
        verbose_name='How many household members live in the '
                     'participants primary home',)

    highest_education = models.CharField(
        verbose_name='Highest education level',
        max_length=30,
        choices=HIGHEST_EDUCATION)

    employment_status = models.CharField(
        verbose_name='Employment Status',
        max_length=33,
        choices=EMPLOYMENT_STATUS)

    employment_status_other = models.CharField(
        verbose_name='Other, specify',
        max_length=33,
        blank=True,
        null=True)

    settlement_type = models.CharField(
        verbose_name='Settlement Type?',
        max_length=30,
        choices=SETTLEMENT_TYPE)

    marital_status = models.CharField(
        verbose_name='Current marital status?',
        max_length=30,
        choices=MARITAL_STATUS)

    marital_status_other = models.CharField(
        verbose_name='Other, specify',
        max_length=30,
        blank=True,
        null=True)

    running_water = models.CharField(
        verbose_name='Is there running water in domicile?',
        max_length=30,
        choices=YES_NO)

    class Meta(CrfModelMixin.Meta):
        app_label = 'esr21_subject'
        verbose_name = 'Demographic Data'
        verbose_name_plural = 'Demographic Data'
