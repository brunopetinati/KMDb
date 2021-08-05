from rest_framework import serializers
from .models import User

# ao usar .ModelSerializer ele já entende que a chave primária id é read_only, no entando isso não 
# acontece com o password

class UserSerializerAccount(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
            "is_superuser",
            "is_staff"
        ]

    # password = serialziers.Charfield(read_only=True)

        extra_kwargs = {'password':{'write_only':True}} 


    # a seguir, o método sobrescrito pertence ao ModelSerializer, e não à classe Meta. 
    # então usamos essa identação
    # validated_data = request
    # def create 'original' tem apenas create, e não create_user
    # original refere-se ao def create de ModelSerializer.

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserSerializerLogin(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()