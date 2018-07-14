from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .forms import PostForm
from .models import ResearchRequest

# Create your views here.

def market_list(request):
	researchrequests = ResearchRequest.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	return render(request, 'market/market_list.html', {'researchrequests':researchrequests})
	
def market_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('market_detail', pk=market.pk)
    else:
        form = PostForm()
    return render(request, 'market/market_edit.html', {'form': form})

def market_edit(request, pk):
	researchrequest = get_object_or_404(ResearchRequest, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
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
    return render(request, 'market/market_detail.html', {'researchrequest': researchrequest})