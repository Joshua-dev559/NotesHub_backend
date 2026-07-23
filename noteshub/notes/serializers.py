from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Note
from categories.serializers import CategorySerializer

# Get the User model dynamically
User = get_user_model()


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True, write_only=True)
    username = serializers.CharField(required=False, allow_blank=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email:
            raise serializers.ValidationError({"email": "This field is required."})

        user = authenticate(
            request=self.context.get("request"),
            email=email,
            password=password,
        )

        if not user or not user.is_active:
            raise serializers.ValidationError({
                "detail": "No active account found with the given credentials."
            })

        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class NoteSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.UUIDField(
        write_only=True,
        required=False
    )

    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "content",
            "category",
            "category_id",
            "is_pinned",
            "is_archived",
            "color",
            "tags",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "created_at",
            "updated_at",
        ]


# Add these new serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8, required=False)
    password2 = serializers.CharField(write_only=True, min_length=8, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'password2', 'first_name', 'last_name']

    def validate(self, data):
        password_confirm = data.get('password_confirm') or data.get('password2')
        if password_confirm is None:
            raise serializers.ValidationError({"password": "Password confirmation is required"})
        if data['password'] != password_confirm:
            raise serializers.ValidationError({"password": "Passwords don't match"})
        data['password_confirm'] = password_confirm
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        validated_data.pop('password2', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user