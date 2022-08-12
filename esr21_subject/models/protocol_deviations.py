from django.db import models
from edc_base.utils import get_utcnow
from edc_base.model_validators.date import datetime_not_future
from edc_protocol.validators import datetime_not_before_study_start
from edc_base.model_mixins import BaseUuidModel
from .model_mixins import SearchSlugModelMixin
from edc_base.model_managers import HistoricalRecords


from edc_search.model_mixins import SearchSlugManager
from edc_base.sites import SiteModelMixin
from .list_models import SubjectIdentifiers


class ProtocolDeviationsManager(SearchSlugManager, models.Manager):

    def get_by_natural_key(self, deviation_name):
        return self.get(deviation_name=deviation_name)

class ProtocolDeviations(SearchSlugModelMixin,
                         SiteModelMixin,
                         BaseUuidModel):
    """A model for protocol deviations
    """
    
    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        default=get_utcnow,
        help_text=('If reporting today, use today\'s date/time, otherwise use '
                    'the date/time this information was reported.'))
    
    deviation_name = models.CharField(
        max_length=250,
        verbose_name='Deviation',
        unique=True,
      )
    
    subject_identifiers = models.ManyToManyField(
        SubjectIdentifiers,
        verbose_name="Subject Identifier's",
        blank=True,
    )
    
    deviation_description = models.TextField(
        max_length=250,
        verbose_name='Deviation Description',
     )
    
    deviation_form_name = models.CharField(
        verbose_name='Form\'s that have deviations',
        max_length=200,)
    
    comment = models.TextField(
        max_length=250,
        verbose_name='Comments',
        blank=True,
        null=True)
    
    history = HistoricalRecords()
    
    objects = ProtocolDeviationsManager()
    
    def __str__(self):
        return self.deviation_name

    def natural_key(self):
        return (self.deviation_name,)

    natural_key.dependencies = ['sites.Site']
    
    def get_search_slug_fields(self):
        return ['deviation_name']
    
    class Meta:
        app_label = 'esr21_subject'
        verbose_name = 'Protocol Deviations'
        verbose_name_plural = 'Protocol Deviations'
