from rest_framework import serializers
from django.contrib.auth import get_user_model

User=get_user_model()

class UserSerializer(serializers.ModelSerializer):
  full_name=serializers.ReadOnlyField()

  class Meta:
    model=User
    fields = [
            'id', 'email', 'username', 'first_name', 'last_name', 'full_name',
            'profile_picture', 'bio', 'role', 'interests',
            'linkedin_url','city', 'country', 'date_joined'
        ]
    read_only_fields=['id','date_joined','full_name']


class RegisterSerializer(serializers.ModelSerializer):
  password=serializers.CharField(write_only=True,min_length=8,style={'input_type':'password'})
  password_confirm=serializers.CharField(write_only=True,min_length=8,style={'input_type':'password'})

  class Meta:
    model=User
    fields=['email','password','password_confirm','first_name','last_name','role','interests']

  def validate(self,attrs):
    if attrs['password']!=attrs['password_confirm']:
      raise serializers.ValidationError({"password":"Password don't match"});
    return attrs
  
  def create(self,validated_data):
    validated_data.pop('password_confirm')

    email = validated_data['email']
    username = email 
    
    user=User.objects.create_user(
      email=email,
        username=username,
          password=validated_data['password'],
          first_name=validated_data.get('first_name', ''),
          last_name=validated_data.get('last_name', ''),
          role=validated_data.get('role', 'attendee'),
          interests=validated_data.get('interests', ''),

    )
    return user
    


class LoginSerializer(serializers.Serializer):
  email=serializers.EmailField()
  password=serializers.CharField(write_only=True,style={'input_type':'password'})

class ProfileUpdateSerializer(serializers.ModelSerializer):
  
  class Meta:
    model=User
    fields=['first_name', 'last_name', 'profile_picture',
            'bio', 'interests', 'linkedin_url', 
            'city', 'country']


  