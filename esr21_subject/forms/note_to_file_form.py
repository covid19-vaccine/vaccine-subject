from django import forms

from ..models import NoteToFile
from ..models import NoteToFileDocs


class NoteToFileForm(forms.ModelForm):
    
    class Meta:
        model = NoteToFile
        fields = '__all__'
        
class NoteToFileDocsForm(forms.ModelForm): 
    
    def has_changed(self):
        return True
    class Meta:
        model = NoteToFileDocs
        fields = '__all__'       
