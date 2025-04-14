from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # 이메일 필드 추가

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email',)




