from rest_framework import serializers

from rakamin_test.apps.users.model import users


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = ['name', 'password', 'mobile_number']

    def create(self, validated_data):
        password1 = validated_data.pop('password', '')
        user = users.objects.create(**validated_data)
        user.set_password(password1)
        user.save()
        return user