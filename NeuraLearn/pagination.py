from rest_framework.pagination import LimitOffsetPagination as LOP

class LimitOffsetPagination(LOP):
    default_limit = 10
    max_limit = 1000