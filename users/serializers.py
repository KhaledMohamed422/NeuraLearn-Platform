from django.contrib.auth.models import Group
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_student', 'is_instructor', 'password')

    def create(self, validated_data):
        is_instructor = validated_data.pop('is_instructor', False)
        user = super().create(validated_data)
        
        if is_instructor:
            instructor_group, created = Group.objects.get_or_create(name='instructor')
            user.groups.add(instructor_group)
            user.save()

        return user
