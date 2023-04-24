from rest_framework.permissions import BasePermission


class IsAFox(BasePermission):
    """
    Is the current user a fox?
    """
    pass