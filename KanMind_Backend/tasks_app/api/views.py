from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Task, Comment
from .serializers import (
    TaskListSerializer, TaskDetailSerializer,
    TaskCreateSerializer, TaskUpdateSerializer,
    CommentSerializer
)
from .permissions import IsBoardMember, IsTaskCreatorOrBoardOwner, IsCommentAuthor


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsBoardMember]
    
    def get_queryset(self):
        return Task.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TaskCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TaskUpdateSerializer
        elif self.action == 'retrieve':
            return TaskDetailSerializer
        return TaskListSerializer
    
    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAuthenticated(), IsBoardMember(), IsTaskCreatorOrBoardOwner()]
        elif self.action == 'create':
            return [IsAuthenticated(), IsBoardMember()]
        return [IsAuthenticated(), IsBoardMember()]
    
    def create(self, request):
        serializer = TaskCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            task = serializer.save()
            return Response(
                TaskListSerializer(task).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        task = self.get_object()
        serializer = TaskUpdateSerializer(
            task,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        return self.update(request, pk)
    
    def destroy(self, request, pk=None):
        task = self.get_object()
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def assigned_to_me(self, request):
        tasks = Task.objects.filter(assignee=request.user)
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def reviewing(self, request):
        tasks = Task.objects.filter(reviewer=request.user)
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data)
    


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsBoardMember]
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        task_id = self.kwargs.get('task_pk')
        return Comment.objects.filter(task_id=task_id).order_by('created_at')
    
    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAuthenticated(), IsBoardMember(), IsCommentAuthor()]
        return [IsAuthenticated(), IsBoardMember()]
    
    def create(self, request, task_pk=None):
        try:
            task = Task.objects.get(id=task_pk)
        except Task.DoesNotExist:
            return Response(
                {'error': 'Task not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = CommentSerializer(
            data=request.data,
            context={'request': request, 'task': task}
        )
        if serializer.is_valid():
            comment = serializer.save()
            return Response(
                CommentSerializer(comment).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, task_pk=None):
        try:
            task = Task.objects.get(id=task_pk)
        except Task.DoesNotExist:
            return Response(
                {'error': 'Task not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        comments = task.comments.all().order_by('created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, task_pk=None, pk=None):
        comment = self.get_object()
        # Check if user is the author
        if comment.author != request.user:
            return Response(
                {'error': 'You can only delete your own comments.'},
                status=status.HTTP_403_FORBIDDEN
            )
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

