class CourseOwnerMixin:
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(owner=self.request.user)