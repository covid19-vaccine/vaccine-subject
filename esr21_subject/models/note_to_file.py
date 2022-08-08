from django.db import models
from edc_base.utils import get_utcnow
from edc_base.model_validators.date import datetime_not_future
from edc_protocol.validators import datetime_not_before_study_start
from django.utils.html import mark_safe

from edc_base.sites import SiteModelMixin
from edc_base.model_mixins import BaseUuidModel

from .model_mixins import SearchSlugModelMixin
from edc_search.model_mixins import SearchSlugManager
from .list_models import SubjectIdentifiers


class NoteToFileManager(SearchSlugManager,models.Manager):

    def get_by_natural_key(self, note_name):
        return self.get(note_name=note_name)

class NoteToFile(SearchSlugModelMixin,
                 SiteModelMixin,BaseUuidModel):
    
    """A model for note to files
    """
    @property
    def related_objects(self):
        return getattr(self, 'note_to_file')
    
    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        default=get_utcnow,
        help_text=('If reporting today, use today\'s date/time, otherwise use '
                    'the date/time this information was reported.'))
    
    note_name = models.CharField(
        max_length=250,
        verbose_name='Note to file name',
    )
    
    note_description = models.TextField(
        max_length=250,
        verbose_name='Note to file description',
    )
    
    subject_identifiers = models.ManyToManyField(
        SubjectIdentifiers,
        verbose_name="Subject Identifier's",
        blank=True,
    )
        
    comment = models.TextField(
        max_length=250,
        verbose_name='Comments',
        blank=True,
        null=True)
    
    objects = NoteToFileManager()
    
    def __str__(self):
        return self.note_name
    
    def natural_key(self):
        return (self.note_name,)
    
    # natural_key.dependencies = ['sites.Site']
    
    def get_search_slug_fields(self):
        fields = []
        fields.append('note_name')
        return fields
        
    class Meta:
        app_label = 'esr21_subject'
        verbose_name = 'Note to file'
        verbose_name_plural = 'Notes to file'
        
        
class NoteToFileDocsManager(models.Manager):

    def get_by_natural_key(self, note_to_file):
        return self.get(note_to_file=note_to_file)        
class NoteToFileDocs(BaseUuidModel):

    notes_to_file = models.ForeignKey(
        NoteToFile,
        on_delete=models.PROTECT,
        related_name='note_to_file')

    def upload_to_path(instance, filename):
        today = get_utcnow().date().strftime('%Y/%m/%d')
        if filename:
            return f'notes_to_file/{today}/{filename}'
        return f'notes_to_file/{today}/'
    
    file_save = models.FileField(upload_to='note_to_file/', blank=True, null=True)
    
    objects = NoteToFileDocsManager()
    
    def natural_key(self):
        return (self.note_to_file,)
    
    user_uploaded = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='user uploaded',)

    datetime_captured = models.DateTimeField(
        default=get_utcnow)

    def ntf_document(self):
            return mark_safe(
                '<embed src="%(url)s" style="border:none" height="100" width="150"'
                'title="note to file"></embed>' % {'url': self.file_save.url})

    ntf_document.short_description = 'Preview'
    ntf_document.allow_tags = True        
