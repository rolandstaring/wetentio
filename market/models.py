from django.db import models
from django.utils import timezone

# Create your models here.

class ResearchRequest(models.Model):
	author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	hypo = models.TextField()
	max_part_nr = models.IntegerField()
	min_par_nr = models.IntegerField()
	end_date = models.DateTimeField(blank=True, null=True)
	created_date = models.DateTimeField(
			default=timezone.now)
	published_date = models.DateTimeField(
			blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title
		
class ResearchParticipant(models.Model):
	author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	researchrequest = models.ForeignKey(ResearchRequest, on_delete=models.CASCADE)
	email = models.CharField("Email adres", max_length=30)
	
	def publish(self):
		self.published_date = timezone.now()
		self.save()
	
	def __str__(self):
		return self.title