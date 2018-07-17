from django import forms
from .models import ResearchRequest, ResearchParticipant

class ResearchForm(forms.ModelForm):

	class Meta:
		model = ResearchRequest
		fields = ('title', 'hypo','max_part_nr','min_part_nr', 'end_date')
		
class ParticipantForm(forms.ModelForm):

	class Meta:
		model = ResearchParticipant
		fields = ('email', 'motivation')