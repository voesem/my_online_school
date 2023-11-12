from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True

        return False


class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Модераторы').exists()


class IsNotModerator(BasePermission):

    def has_permission(self, request, view):
        return not request.user.groups.filter(name='Модераторы').exists()
