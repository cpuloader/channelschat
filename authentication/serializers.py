from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

from authentication.models import Account


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    picture = serializers.ImageField(max_length=None, allow_empty_file=False, 
            use_url=True, required=False, allow_null=True)

    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'tagline', 'password',
                  'confirm_password', 'picture', 'enabled', 'is_online')
        read_only_fields = ('created_at', 'updated_at', 'is_online')

    def create(self, validated_data):
        password = validated_data.get('password', None)
        if password:
            instance = Account.objects.create(**validated_data)
            instance.set_password(password)
        return instance

    def update(self, instance, validated_data):
        #print(validated_data);
        instance.email = validated_data.get('email', instance.email).lower()
        instance.username = validated_data.get('username', instance.username)
        instance.tagline = validated_data.get('tagline', instance.tagline)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.save()
        password = validated_data.get('password', None)
        confirm_password = validated_data.get('confirm_password', None)

        if password and confirm_password and password == confirm_password:
            instance.set_password(password)
            instance.save()

        update_session_auth_hash(self.context.get('request'), instance)
        return instance

