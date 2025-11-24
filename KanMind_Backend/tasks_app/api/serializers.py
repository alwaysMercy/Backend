from rest_framework import serializers
from ..models import Task, Comment
from auth_app.api.serializers import UserSerializer
from boards_app.models import Board


class TaskListSerializer(serializers.ModelSerializer):
    assignee = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    
    class Meta:
        model = Task
        fields = (
            'id', 'board', 'title', 'description', 'status', 'priority',
            'assignee', 'reviewer', 'due_date', 'comments_count'
        )


class TaskDetailSerializer(serializers.ModelSerializer):
    assignee = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = (
            'id', 'board', 'title', 'description', 'status', 'priority',
            'assignee', 'reviewer', 'due_date'
        )


class TaskCreateSerializer(serializers.ModelSerializer):
    assignee_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    reviewer_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    assignee = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    
    class Meta:
        model = Task
        fields = (
            'id', 'board', 'title', 'description', 'status', 'priority',
            'assignee_id', 'reviewer_id', 'assignee', 'reviewer', 
            'due_date', 'comments_count'
        )
    
    def validate(self, data):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        board_id = data.get('board')
        assignee_id = data.get('assignee_id')
        reviewer_id = data.get('reviewer_id')
        
        if board_id:
            try:
                board = Board.objects.get(id=board_id.id if hasattr(board_id, 'id') else board_id)
                
                # Validate assignee is board member
                if assignee_id:
                    try:
                        assignee = User.objects.get(id=assignee_id)
                        if assignee != board.owner and assignee not in board.members.all():
                            raise serializers.ValidationError({
                                'assignee_id': 'Assignee must be a member of the board.'
                            })
                    except User.DoesNotExist:
                        raise serializers.ValidationError({'assignee_id': 'User does not exist.'})
                
                # Validate reviewer is board member
                if reviewer_id:
                    try:
                        reviewer = User.objects.get(id=reviewer_id)
                        if reviewer != board.owner and reviewer not in board.members.all():
                            raise serializers.ValidationError({
                                'reviewer_id': 'Reviewer must be a member of the board.'
                            })
                    except User.DoesNotExist:
                        raise serializers.ValidationError({'reviewer_id': 'User does not exist.'})
            except Board.DoesNotExist:
                raise serializers.ValidationError({'board': 'Board does not exist.'})
        
        return data
    
    def create(self, validated_data):
        assignee_id = validated_data.pop('assignee_id', None)
        reviewer_id = validated_data.pop('reviewer_id', None)
        
        task = Task.objects.create(
            **validated_data,
            created_by=self.context['request'].user,
            assignee_id=assignee_id,
            reviewer_id=reviewer_id
        )
        return task


class TaskUpdateSerializer(serializers.ModelSerializer):
    assignee_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    reviewer_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    assignee = UserSerializer(read_only=True)
    reviewer = UserSerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = (
            'id', 'title', 'description', 'status', 'priority',
            'assignee_id', 'reviewer_id', 'assignee', 'reviewer', 'due_date'
        )
    
    def validate(self, data):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if self.instance:
            board = self.instance.board
            
            # Validate assignee is board member
            assignee_id = data.get('assignee_id')
            if assignee_id is not None:
                try:
                    assignee = User.objects.get(id=assignee_id)
                    if assignee != board.owner and assignee not in board.members.all():
                        raise serializers.ValidationError({
                            'assignee_id': 'Assignee must be a member of the board.'
                        })
                except User.DoesNotExist:
                    raise serializers.ValidationError({'assignee_id': 'User does not exist.'})
            
            # Validate reviewer is board member
            reviewer_id = data.get('reviewer_id')
            if reviewer_id is not None:
                try:
                    reviewer = User.objects.get(id=reviewer_id)
                    if reviewer != board.owner and reviewer not in board.members.all():
                        raise serializers.ValidationError({
                            'reviewer_id': 'Reviewer must be a member of the board.'
                        })
                except User.DoesNotExist:
                    raise serializers.ValidationError({'reviewer_id': 'User does not exist.'})
        
        return data
    
    def update(self, instance, validated_data):
        assignee_id = validated_data.pop('assignee_id', None)
        reviewer_id = validated_data.pop('reviewer_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if assignee_id is not None:
            instance.assignee_id = assignee_id
        if reviewer_id is not None:
            instance.reviewer_id = reviewer_id
        
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.fullname', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'created_at', 'author', 'content')
        read_only_fields = ('id', 'created_at', 'author')
    
    def create(self, validated_data):
        task = self.context['task']
        comment = Comment.objects.create(
            task=task,
            author=self.context['request'].user,
            **validated_data
        )
        return comment

