from rest_framework.permissions import BasePermission


class IsAFox(BasePermission):
    """
    Is the current user a fox?
    """
    
    def has_permission(self, request, view):
        """
        Checks if the current user is a fox; a fox user has username as 'reynard'
        """
        
        return request.user.username == 'reynard'