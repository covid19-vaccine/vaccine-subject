from django.db import models
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_validators import datetime_not_future
from edc_base.sites import SiteModelMixin
from edc_base.utils import get_utcnow
from edc_constants.choices import YES_NO
from edc_constants.constants import NO
from edc_identifier.model_mixins import NonUniqueSubjectIdentifierFieldMixin
from edc_search.model_mixins import SearchSlugManager

from ..identifiers import ScreeningIdentifier
from .eligibility import Eligibility
from .model_mixins import SearchSlugModelMixin


class EligibilityConfirmationManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, screening_identifier):
        return self.get(screening_identifier=screening_identifier)


class EligibilityConfirmation(NonUniqueSubjectIdentifierFieldMixin,
                              SiteModelMixin,
                              SearchSlugModelMixin, BaseUuidModel):
    identifier_cls = ScreeningIdentifier

    screening_identifier = models.CharField(
        verbose_name='Eligibility Identifier',
        max_length=36,
        unique=True,
        editable=False)

    report_datetime = models.DateTimeField(
        verbose_name='Report Date and Time',
        default=get_utcnow,
        validators=[datetime_not_future],
        help_text='Date and time of report.')

    # TODO: Asked a question about what type of answer
    any_vaccine_receipt = models.CharField(
        verbose_name=('Any receipt of, or planned receipt of any COVID-19 vaccine '
                      'booster dose, or any medications, or investigational '
                      'products indicated for the prevention of SARS-CoV-2 '
                      'infection or treatment of COVID-19?'),
        help_text=('For study participants who become hospitalised with COVID-19,'
                   ' receipt of licensed treatment options and/or participation'
                   ' in investigational treatment studies is permitted.'),
        choices=YES_NO,
        max_length=3,
    )

    participating_in_other_studies = models.CharField(
        verbose_name='Is the participant participating in other studies?',
        max_length=3,
        choices=YES_NO,
        default=NO,)

    age_in_years = models.PositiveIntegerField(
        verbose_name='What is the participants age?',
        help_text='(Years)',)

    received_vaccines = models.CharField(
        verbose_name='Has the participant received any vaccine other than '
                     'licensed influenza vaccines within 30 days prior to '
                     'and after administration of study intervention (i.e the '
                     'first, second and booster doses)?',
        max_length=10,
        choices=YES_NO,
        help_text='If Yes, participant is not eligible')

    ineligibility = models.TextField(
        verbose_name="Reason not eligible",
        max_length=150,
        null=True,
        editable=False)

    is_eligible = models.BooleanField(
        default=False,
        editable=False)

    # is updated via signal once subject is consented
    is_consented = models.BooleanField(
        default=False,
        editable=False)

    history = HistoricalRecords()

    objects = EligibilityConfirmationManager()

    def __str__(self):
        return self.screening_identifier

    def natural_key(self):
        return (self.screening_identifier,)

    natural_key.dependencies = ['sites.Site']

    def save(self, *args, **kwargs):
        eligibility_criteria = Eligibility(self.age_in_years,
                                           self.received_vaccines,
                                           self.any_vaccine_receipt,
                                           self.participating_in_other_studies)
        self.is_eligible = eligibility_criteria.is_eligible
        self.ineligibility = eligibility_criteria.error_message
        if not self.screening_identifier:
            self.screening_identifier = self.identifier_cls().identifier
        super().save(*args, **kwargs)

    def get_search_slug_fields(self):
        fields = super().get_search_slug_fields()
        fields.append('screening_identifier')
        return fields

    class Meta:
        app_label = 'esr21_subject'
        verbose_name = 'Eligibility Confirmation'
        verbose_name_plural = 'Eligibility Confirmation'
