from rest_framework import serializers
from .helpers.validators import validate_password

from rest_framework.exceptions import ValidationError

from . import models


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializers for user profile objests"""

    class Meta:
        model = models.User
        fields = ('id', 'email', 'name', 'password', 'is_staff')
        extra_kwargs = {'password': {'write_only': True},
                        'is_staff': {'read_only': True}}
    
    def create(self, validated_data):
        """Create and return a new user"""

        user = models.User(
            email = validated_data['email'],
            name = validated_data['name']
        )
        
        user.set_password(validated_data['password'])
        user.save()

        return user
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        # print(validated_data)
        if validated_data.get('password'):
            validation_errors = validate_password(validated_data.get('password'))
            if validation_errors:
                raise ValidationError({"password": " ".join(validation_errors)})
            
            instance.set_password(validated_data.get('password'))

        instance.save()

        return instance


class SignUpSerializer(serializers.Serializer):
    """Serializer for user signup"""
    email = serializers.EmailField(max_length=255)
    name = serializers.CharField(max_length=255)
