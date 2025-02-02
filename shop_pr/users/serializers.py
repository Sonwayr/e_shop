from rest_framework import serializers

from .models import CustomUser, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'house_number', 'city', 'country', 'zip_code']


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(source='addresses')
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'password2', 'first_name', 'last_name', 'phone_number',
                  'address']

    def validate(self, data):
        """
        Check that the two password fields match.
        """
        if 'password' in data and 'password2' in data:
            if data['password'] != data['password2']:
                raise serializers.ValidationError({"password": "The two password fields must match."})

        # Check if username or password is being updated in PATCH or PUT method
        request_method = self.context['request'].method
        if request_method in ['PATCH', 'PUT']:
            if 'username' in data:
                raise serializers.ValidationError({"username": "You cannot update the username."})
            if 'password' in data or 'password2' in data:
                raise serializers.ValidationError({"password": "You cannot update the password."})

        return data

    def create(self, validated_data):
        address_data = validated_data.pop('addresses', None)
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number', ''),
        )

        if address_data:
            Address.objects.create(user=user, **address_data)

        return user
