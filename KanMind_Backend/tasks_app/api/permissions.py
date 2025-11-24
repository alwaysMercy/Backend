from rest_framework import permissions


class IsBoardMember(permissions.BasePermission):
    """
    Permission to check if user is member or owner of the board.
    """
    
    def has_permission(self, request, view):
        if request.method == 'POST':
            board_id = request.data.get('board')
            if board_id:
                try:
                    from boards_app.models import Board
                    board = Board.objects.get(id=board_id)
                    return board.owner == request.user or request.user in board.members.all()
                except (Board.DoesNotExist, ValueError, TypeError):
                    return False
        return True
    
    def has_object_permission(self, request, view, obj):
        board = obj.task.board
        return board.owner == request.user or request.user in board.members.all()


class IsTaskCreatorOrBoardOwner(permissions.BasePermission):
    """
    Permission to check if user is task creator or board owner.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return obj.created_by == request.user or obj.board.owner == request.user
        return True


class IsCommentAuthor(permissions.BasePermission):
    """
    Permission to check if user is the comment author.
    """
    
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return obj.author == request.user
        return True

