# from rest_framework import serializers
# from .models import User

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
    
#     class Meta:
#         model =User
#         fields =[
#             "email",
#             "first_name",
#             "last_name",
#             "password",
#         ]
    
#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)

#     def validate_email(self, value):
#         if not value:
#             raise serializers.ValidationError("Email is required")
#         return value

from rest_framework import serializers

from .models import User


class RegisterSerializer(
    serializers.ModelSerializer
):

    password = serializers.CharField(
        write_only=True
    )

    class Meta:

        model = User

        fields = [
            "email",
            "first_name",
            "last_name",
            "password",
        ]

    def create(self, validated_data):

        return User.objects.create_user(
            **validated_data
        )
    