from django import forms
from .models import ResearchRequest

class PostForm(forms.ModelForm):

    class Meta:
        model = ResearchRequest
        fields = ('title', 'hypo','max_part_nr','min_par_nr', 'end_date')