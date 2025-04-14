from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from .models import User

class CustomUserDetailsSerializer(UserDetailsSerializer):

    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'nickname')
        
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'nickname']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        print(validated_data)
        nickname = validated_data.pop('nickname', None)
        user = User.objects.create_user(**validated_data)
        if nickname:
            user.nickname = nickname
            user.save()
        return user
    
    def save(self, **kwargs):
        validated_data = self.validated_data
        return self.create(validated_data)