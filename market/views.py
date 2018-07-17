from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect
from .forms import ResearchForm, ParticipantForm
from .models import ResearchRequest, ResearchParticipant

# Create your views here.

def market_list(request):
	researchrequests = ResearchRequest.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'market/market_list.html', {'researchrequests':researchrequests})
	
def participant_add(request, pk):
	researchrequest = get_object_or_404(ResearchRequest, pk=pk)
	if request.method == "POST":
		form = ParticipantForm(request.POST)
		if form.is_valid():
			researchparticipant = form.save(commit=False)
			researchparticipant.author = request.user
			researchparticipant.researchrequest = researchrequest
			researchparticipant.save()
			return redirect('market_detail', pk=researchrequest.pk)
	else:
		form = ParticipantForm()
	return render(request, 'market/add_participant.html', {'form': form, 'researchrequest':researchrequest })	
			
def market_new(request):
	if request.method == "POST":
		form = ResearchForm(request.POST)
		if form.is_valid():
			researchrequest = form.save(commit=False)
			researchrequest.author = request.user
			researchrequest.published_date = timezone.now()
			researchrequest.save()
			return redirect('market_detail', pk=researchrequest.pk)
	else:
		form = ResearchForm()
	return render(request, 'market/market_edit.html', {'form': form})

def market_edit(request, pk):
	researchrequest = get_object_or_404(ResearchRequest, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=researchrequest)
		if form.is_valid():
			researchrequest = form.save(commit=False)
			researchrequest.author = request.user
			researchrequest.published_date = timezone.now()
			researchrequest.save()
			return redirect('market_detail', pk=researchrequest.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'market/market_edit.html', {'form': form})
	
def market_detail(request, pk):
	researchrequest = get_object_or_404(ResearchRequest, pk=pk)
	researchparticipants = ResearchParticipant.objects.filter(researchrequest_id=pk)
	return render(request, 'market/market_detail.html', {'researchrequest': researchrequest, 'researchparticipants': researchparticipants })