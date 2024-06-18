from rest_framework.permissions import BasePermission, DjangoModelPermissions
from users.models import UserAccount as User

class IsModuleOwnerPermission(DjangoModelPermissions, BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.course.owner == request.user

class IsInstructorPermission(BasePermission):
    def has_permission(self, request, view):
        print(request.user)
        print(request.user.groups.filter(name='Instructors').exists())
        return request.user.groups.filter(name='Instructors').exists()