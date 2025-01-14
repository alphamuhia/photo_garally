from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Photo, UserProfile, PhotoInteraction
from .forms import RegistrationForm, LoginForm, PhotoForm, CommentForm, ProfileForm, UserProfile
from django.db import transaction
from django.contrib.auth.models import User



def home(request):
    photos = Photo.objects.all()
    return render(request, 'home.html', {'photos': photos})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            UserProfile.objects.create(user=user)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                return HttpResponse('Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
@transaction.atomic
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, 'profile.html', {'form': form, 'user_profile': user_profile})

def user_profile_view(request):
    user_profile = request.user.profile 
    user_form = ProfileForm(instance=user_profile)

    if request.method == "POST":
        user_form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid():
            user_form.save()

    return render(request, 'profile.html', {
        'user': request.user,
        'user_profile': user_profile,
        'user_form': user_form,
    })


@login_required
def add_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user 
            photo.save()
            return redirect('home')
    else:
        form = PhotoForm()
    return render(request, 'add_photo.html', {'form': form})


def photo_details(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    comments = photo.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.photo = photo
            comment.save()
            return redirect('photo_details', photo_id=photo_id)
    else:
        form = CommentForm()
    return render(request, 'photo_details.html', {'photo': photo, 'comments': comments, 'form': form})

@login_required
def like_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    interaction = PhotoInteraction.objects.filter(user=request.user, photo=photo).first()

    if interaction:
        if interaction.interaction_type == 'like':
            interaction.delete()
            photo.likes -= 1
        else:
            interaction.interaction_type = 'like'
            interaction.save()
            photo.likes += 1
            photo.dislikes -= 1
    else:
        PhotoInteraction.objects.create(user=request.user, photo=photo, interaction_type='like')
        photo.likes += 1

    photo.save()
    return redirect('home')

@login_required
def dislike_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    interaction = PhotoInteraction.objects.filter(user=request.user, photo=photo).first()

    if interaction:
        if interaction.interaction_type == 'dislike':
            interaction.delete()
            photo.dislikes -= 1
        else:
            interaction.interaction_type = 'dislike'
            interaction.save()
            photo.dislikes += 1
            photo.likes -= 1
    else:
        PhotoInteraction.objects.create(user=request.user, photo=photo, interaction_type='dislike')
        photo.dislikes += 1

    photo.save()
    return redirect('home')

