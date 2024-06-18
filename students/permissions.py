from rest_framework.permissions import BasePermission

# check if the user performing the request is present in the students relationship of the Course object.
class IsAdminOrEnrolled(BasePermission):
    message = 'You Must Enroll this course'

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser:
            # if the user is admin then 
            return True
        return obj.students.filter(id=request.user.id).exists()
    

class IsAdminOrEnrolledModule(BasePermission):
    message = 'You Must Enroll this course'

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser:
            # if the user is admin then 
            return True
        return obj.course.students.filter(id=request.user.id).exists()