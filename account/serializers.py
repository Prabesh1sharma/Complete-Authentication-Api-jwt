from xml.dom import ValidationErr
from django.forms import ValidationError
from rest_framework import serializers
from account.models import User 
# to generate uid on the basis of user id
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from account.utils import Util

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = User
        fields =['email', 'name', 'password', 'password2', 'tc']
        extra_kwargs={
            'password':{'write_only':True}
        }
        # Validating Password and confirm password while resgistration
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError('Password and confirm Password does not match')
        return attrs
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
#serializer for the Email verification
class SendVerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']
    def validate(self, attrs):
        email= attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email = email)
            uid= urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Email verification Token', token)
            link = 'http://localhost:8000/api/user/reset/'+uid+'/'+token
            print('Email Verification', link)
            #send Email
            body = 'Click on the link to verify your Account'+link
            data = {
                'subject': 'Verify your Email and account',
                'body':body,
                'to_email':user.email
            }
            Util.send_email(data)

            return attrs

        else:
            raise ValidationErr('You did not Provide the valid Email')
        
class UserVerifySerializer(serializers.Serializer):
    tc =serializers.BooleanField()
    class Meta:
        fields = ['tc']


    def validate(self, attrs):
        try:
            tc = attrs.get('tc')

            uid= self.context.get('uid')
            token= self.context.get('token')
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationError('Token is not valid or Expired')
                
            user.tc=tc
            user.save()

            
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError('Token is not valid or Expired')
        
#end of Email verification
    


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id', 'email','name']


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields= ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user= self.context.get('user')
        if password != password2:
            raise serializers.ValidationError('Password and confirm Password does not match')
        user.set_password(password)
        user.save()

        
        return attrs
    

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']
    def validate(self, attrs):
        email= attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email = email)
            uid= urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'http://localhost:8000/api/user/reset/'+uid+'/'+token
            print('Password Reset Link', link)
            #send Email
            body = 'Click Following link to Reset Your Password'+link
            data = {
                'subject': 'Reset your Password',
                'body':body,
                'to_email':user.email
            }
            Util.send_email(data)

            return attrs

        else:
            raise ValidationErr('You are not a Registered User')
        
class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields= ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid= self.context.get('uid')
            token= self.context.get('token')
            if password != password2:
                raise serializers.ValidationError('Password and confirm Password does not match')
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationError('Token is not valid or Expired')
                
            user.set_password(password)
            user.save()

            
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValidationError('Token is not valid or Expired')



