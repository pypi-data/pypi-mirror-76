from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        is_not_anonymous = str(request.user) != 'AnonymousUser'
        is_active = request.user.is_active
        return is_not_anonymous and is_active
