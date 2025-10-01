from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Petition, Vote


def index(request):
    template_data = {
        'title': 'Petitions',
        'petitions': Petition.objects.order_by('-created_at'),
    }
    return render(request, 'petitions/index.html', {'template_data': template_data})


@login_required
def create(request):
    if request.method == 'GET':
        template_data = {
            'title': 'New Petition',
        }
        return render(request, 'petitions/create.html', {'template_data': template_data})
    elif request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        if not title:
            template_data = {
                'title': 'New Petition',
                'error': 'Title is required.',
            }
            return render(request, 'petitions/create.html', {'template_data': template_data})
        p = Petition(title=title, description=description, created_by=request.user)
        p.save()
        return redirect('petitions.show', id=p.id)


def show(request, id):
    petition = get_object_or_404(Petition, id=id)
    user_vote = None
    if request.user.is_authenticated:
        user_vote = Vote.objects.filter(petition=petition, user=request.user).first()

    template_data = {
        'title': petition.title,
        'petition': petition,
        'yes_count': petition.yes_count,
        'no_count': petition.no_count,
        'user_vote': user_vote,
    }
    return render(request, 'petitions/show.html', {'template_data': template_data})


@login_required
def vote_yes(request, id):
    petition = get_object_or_404(Petition, id=id)
    Vote.objects.update_or_create(petition=petition, user=request.user, defaults={'value': True})
    return redirect('petitions.show', id=id)


@login_required
def vote_no(request, id):
    petition = get_object_or_404(Petition, id=id)
    Vote.objects.update_or_create(petition=petition, user=request.user, defaults={'value': False})
    return redirect('petitions.show', id=id)
