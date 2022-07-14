from django.contrib import admin
# from edc_model_admin import TabularInlineMixin, audit_fieldset_tuple
from edc_model_admin import TabularInlineMixin, audit_fieldset_tuple

from ..admin_site import esr21_subject_admin
from ..models import NoteToFile
# NoteToFileDocs
from ..forms import NoteToFileForm
# NoteToFileDocsForm
from .modeladmin_mixins import ModelAdminMixin


# add the inline
# class NoteToFileDocsInline(TabularInlineMixin, admin.TabularInline):
#     model = NoteToFileDocs
#     form = NoteToFileDocsForm
#     extra = 0
#     min_num = 1
    
#     fields = ('ntf_document', 'file_save', 'user_uploaded', 'datetime_captured',
#               'modified', 'hostname_created',)

#     def get_readonly_fields(self, request, obj=None):
#         fields = super().get_readonly_fields(request, obj)
#         fields = ('ntf_document', 'datetime_captured', 'user_uploaded') + fields

#         return fields


@admin.register(NoteToFile, site=esr21_subject_admin)
class NoteToFileAdmin(ModelAdminMixin, admin.ModelAdmin):
    
    form = NoteToFileForm
    fieldsets = (
        (None, {
            "fields": (
                "report_datetime",
                "note_name",
                "note_description",
                "subject_identifiers",
                "comment",
            ),
        }),
        audit_fieldset_tuple
    )
    
    list_display = [
        'report_datetime', 'note_name',]
    
    filter_horizontal = ('subject_identifiers',)
    
    # inlines = [NoteToFileDocsInline]