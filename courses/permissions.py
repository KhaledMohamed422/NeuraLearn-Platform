from rest_framework.permissions import BasePermission, DjangoModelPermissions

# TODO Create IsInstructorUserPermission

class IsCourseOwnerPermission(DjangoModelPermissions, BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the course
        return obj.owner == request.user

class IsModuleOwnerPermission(DjangoModelPermissions, BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.course.owner == request.user