from rest_framework import serializers
from .models import User, Property, Transaction

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'image', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

class PropertySerializer(serializers.ModelSerializer):
    seller = UserSerializer(read_only=True)

    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

class TransactionSerializer(serializers.ModelSerializer):
    property = PropertySerializer(read_only=True)
    buyer = UserSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'property', 'buyer', 'amount', 'transaction_date', 'payment_status', 'payment_method', 'payment_date']
        read_only_fields = ['id', 'transaction_date']
