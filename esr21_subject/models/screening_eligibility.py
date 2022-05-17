from django.db import models
from edc_base.model_fields import OtherCharField
from edc_identifier.model_mixins import UniqueSubjectIdentifierModelMixin
from edc_search.model_mixins import SearchSlugManager
from edc_base.model_mixins import BaseUuidModel
from esr21_subject.models.second_eligibility import SecondEligibility
from .model_mixins import SearchSlugModelMixin
from edc_base.model_managers import HistoricalRecords

from edc_constants.choices import YES_NO
from edc_constants.constants import NO
from .list_models import Symptoms, Diseases, SymptomaticInfections
from edc_base.utils import get_utcnow
from edc_base.model_validators import datetime_not_future
from edc_base.sites import SiteModelMixin


class EligibilityConfirmationManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, screening_identifier):
        return self.get(screening_identifier=screening_identifier)


class ScreeningEligibility(UniqueSubjectIdentifierModelMixin, SiteModelMixin,
                           SearchSlugModelMixin, BaseUuidModel):

    report_datetime = models.DateTimeField(
        verbose_name='Report Date and Time',
        default=get_utcnow,
        validators=[datetime_not_future],
        help_text='Date and time of report.')

    substance_hypersensitivity = models.CharField(
        verbose_name=('Any hypersensitivity to the active substance or to any of the '
                      'excipients?'),
        choices=YES_NO,
        max_length=3,
        default=NO
    )

    pregnancy_status = models.CharField(
        verbose_name=('Are you pregnant or nursing or do you plan to get pregnant in the next '
                      '3 months?'),
        max_length=3,
        choices=YES_NO,
        default=NO
    )

    # ADDED QUESTIONS FROM THE DOC
    thrombosis_or_thrombocytopenia = models.CharField(
        verbose_name=('Does individuals have any risk factors for or a reported history of '
                      'thrombosis and/or thrombocytopenia?'),
        max_length=3,
        choices=YES_NO,
        default=NO,
    )

    clinical_bleeding = models.CharField(
        verbose_name=('Ever experienced clinically significant bleeding, or prior history '
                      'of significant bleeding or bruising following intramuscular injections '
                      'or venepuncture?'),
        max_length=20,
        choices=YES_NO,
        default=NO,
        help_text=('(eg, factor deficiency, coagulopathy, or platelet disorder) '),
    )

    guillain_barre_syndrome = models.CharField(
        verbose_name='Any history of Guillain-Barré syndrome?',
        max_length=3,
        choices=YES_NO,
        default=NO)

    suspected_immuno_condition = models.CharField(
        verbose_name=('Any confirmed or suspected immunosuppressive or immunodeficient state '
                      '(including Asplenia)?'),
        max_length=3,
        choices=YES_NO,
        default=NO
    )

    comorbidities = models.ManyToManyField(
        Diseases,
        verbose_name='Comorbidities',
        blank=True,
    )

    comorbidities_other = models.CharField(
        verbose_name='Other specify',
        max_length=50,
        blank=True,
        null=True)

    covid_symptoms = models.ManyToManyField(
        Symptoms,
        verbose_name='Did the participant experience any symptoms?',
        blank=True)

    symptoms_other = models.TextField(
        verbose_name='If other specify',
        blank=True,
        null=True)

    is_eligible = models.BooleanField(
        default=False,
    )

    ineligibility = models.TextField(
        verbose_name="Reason not eligible",
        max_length=150,
        null=True,
    )

    # covid symptomatic test
    symptomatic_infections_experiences = models.CharField(
        verbose_name='Are you currently experiencing COVID-like symptoms',
        max_length=20,
        choices=YES_NO, )

    symptomatic_infections = models.ManyToManyField(
        SymptomaticInfections,
        verbose_name='Symptomatic infections ',
        blank=True
    )

    symptomatic_infections_other = OtherCharField()

    childbearing_potential = models.CharField(
        verbose_name='Is woman of childbearing potential (WOCBP)?',
        max_length=150,
        choices=YES_NO,
        default=NO
    )

    birth_control = models.CharField(
        verbose_name='Is the participant willing to use contraceptive consistent with standard of care for birth control from Day 0?',
        max_length=150,
        choices=YES_NO,
        blank=True
    )

    birthcontrol_agreement = models.CharField(
        verbose_name='Is the participant willing to use contraceptive consistent with standard of care for 30 Days after the second dose?',
        max_length=150,
        choices=YES_NO,
        blank=True
    )

    history = HistoricalRecords()

    objects = EligibilityConfirmationManager()

    def __str__(self):
        return self.subject_identifier

    def natural_key(self):
        return (self.subject_identifier,)

    natural_key.dependencies = ['sites.Site']

    def save(self, *args, **kwargs):
        screening_eligibility = SecondEligibility(
            substance_hypersensitivity=self.substance_hypersensitivity,
            pregnancy_status=self.pregnancy_status,
            thrombosis_or_thrombocytopenia=self.thrombosis_or_thrombocytopenia,
            guillain_barre_syndrome=self.guillain_barre_syndrome,
            suspected_immuno_condition=self.suspected_immuno_condition,
            clinical_bleeding=self.clinical_bleeding,
            symptoms_other=self.symptoms_other,
            comorbidities_other=self.comorbidities_other,
            childbearing_potential=self.childbearing_potential,
            birth_control=self.birth_control,
            birthcontrol_agreement=self.birthcontrol_agreement,
            symptomatic_infections_experiences=self.symptomatic_infections_experiences,
            symptomatic_infections_other=self.symptomatic_infections_other
        )
        self.is_eligible = screening_eligibility.is_eligible
        self.ineligibility = screening_eligibility.error_message
        if not self.subject_identifier:
            self.subject_identifier = self.identifier_cls().identifier
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'esr21_subject'
        verbose_name = 'Screening Eligibility'
        verbose_name_plural = 'Screening Eligibility'
