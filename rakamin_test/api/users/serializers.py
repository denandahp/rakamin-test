from rest_framework import serializers

from rakamin_test.apps.users.model import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'password', 'mobile_number']

    def create(self, validated_data):
        password1 = validated_data.pop('password', '')
        user = User.objects.create(**validated_data)
        user.set_password(password1)
        user.save()
        return user