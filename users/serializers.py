from django.contrib.auth.models import Group
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_student', 'is_instructor', 'password')

    def create(self, validated_data):
        # Extract the custom fields
        is_instructor = validated_data.pop('is_instructor', False)
        is_student = validated_data.pop('is_student', False)

        # Create the user
        user = super().create(validated_data)
        user.is_instructor = is_instructor
        user.is_student = is_student
        user.save()

        # Add the user to the 'instructor' group if is_instructor is True
        if is_instructor:
            try:
                instructor_group, created = Group.objects.get_or_create(name='Instructors')
                user.groups.add(instructor_group)
                user.save()
                print(f"User {user.email} added to 'instructor' group.")
            except Exception as e:
                print(f"Failed to add user {user.email} to 'instructor' group: {e}")

        return user
