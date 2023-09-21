from rest_framework import permissions


class IsOwnerOrIsAuthenticatedReadOnly(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
