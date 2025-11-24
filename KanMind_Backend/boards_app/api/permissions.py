from rest_framework import permissions


class IsBoardOwnerOrMember(permissions.BasePermission):
    """
    Permission to check if user is owner or member of the board.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user in obj.members.all()


class IsBoardOwner(permissions.BasePermission):
    """
    Permission to check if user is owner of the board.
    """
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

