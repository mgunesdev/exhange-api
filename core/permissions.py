from rest_framework.permissions import BasePermission, SAFE_METHODS

from core.models import User


class IsOwnerOrReadOnly(BasePermission):
    message = 'You must be the owner of this object'
    mySafeMethod = ['GET']

    def has_permission(self, request, view):
        if request.method in self.mySafeMethod:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user


class IsStaffOrSuperUser(BasePermission):
    message = "You must be the staff user"

    def has_permission(self, request, view):
        return request.user.is_staff or request.user.is_superuser


class IsOwner(BasePermission):
    message = 'You must be the owner of this object'

    def has_object_permission(self, request, view, obj):
        if type(obj) is User:
            return obj == request.user
        return obj.user == request.user