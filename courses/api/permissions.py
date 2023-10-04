from rest_framework.permissions import BasePermission

# check if the user performing the request is present in the students relationship of the Course object.
class IsEnrolled(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.students.filter(id=request.user.id).exists()