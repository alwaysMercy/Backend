from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.db import models
from ..models import Board
from .serializers import (
    BoardListSerializer, BoardDetailSerializer, 
    BoardCreateSerializer, BoardUpdateSerializer
)
from .permissions import IsBoardOwnerOrMember, IsBoardOwner
from auth_app.api.serializers import UserSerializer

User = get_user_model()


class BoardViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(
            models.Q(owner=user) | models.Q(members=user)
        ).distinct()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return BoardListSerializer
        elif self.action == 'retrieve':
            return BoardDetailSerializer
        elif self.action == 'create':
            return BoardCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return BoardUpdateSerializer
        return BoardListSerializer
    
    def get_permissions(self):
        if self.action == 'destroy':
            return [IsAuthenticated(), IsBoardOwner()]
        elif self.action in ['update', 'partial_update', 'retrieve']:
            return [IsAuthenticated(), IsBoardOwnerOrMember()]
        return [IsAuthenticated()]
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        board = self.get_object()
        serializer = BoardDetailSerializer(board)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = BoardCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            board = serializer.save()
            return Response(
                BoardListSerializer(board).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        board = self.get_object()
        serializer = BoardUpdateSerializer(
            board,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        return self.update(request, pk)
    
    def destroy(self, request, pk=None):
        board = self.get_object()
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def email_check(request):
    email = request.query_params.get('email', None)
    if not email:
        return Response(
            {'error': 'Email parameter is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(email=email)
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_200_OK
        )
    except User.DoesNotExist:
        return Response(
            {'error': 'Email not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

