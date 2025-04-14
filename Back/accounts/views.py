from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from dj_rest_auth.views import LoginView
from .serializers import CustomUserDetailsSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# 닉네임 디버그
from .serializers import CustomUserSerializer
from dj_rest_auth.registration.views import RegisterView
from rest_framework.response import Response
from rest_framework import status

class CustomLoginView(LoginView):
    def get_response(self):
        response = super().get_response()
        response.data.update({
            'user_id': self.user.id,
            'user_name': self.user.username,
            'user_email': self.user.email,
            'nickname': self.user.nickname,
        })
        return response
    
@api_view(['GET'])    
def CustomUserView(request, user_id):
    User = get_user_model()
    person = User.objects.get(pk=user_id)
    serializer = CustomUserDetailsSerializer(person)
    return Response(serializer.data)

class CustomRegisterView(RegisterView):
    serializer_class = CustomUserSerializer
    def create(self, request, *args, **kwargs):
        print('CustomRegisterView is called')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

### 여기서부턴 의미 없음 ###

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')

    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('movies:index')

def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

@login_required
def account_delete(request):
    request.user.delete()
    return redirect('movies:index')

@login_required
def account_update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)

@login_required
def change_password(request, user_pk):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('movies:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)

def profile(request,user_pk):
    User = get_user_model()
    person = User.objects.get(pk=user_pk)
    context = {
        'person': person,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def follow(request,user_pk):
    User = get_user_model()
    person = User.objects.get(pk=user_pk)
    if person != request.user:
        if request.user in person.followers.all():
            person.followers.remove(request.user)
        else:
            person.followers.add(request.user)
    return redirect('accounts:profile', person.pk)

