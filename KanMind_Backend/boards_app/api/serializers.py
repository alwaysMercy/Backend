from rest_framework import serializers
from ..models import Board
from auth_app.api.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class BoardListSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    member_count = serializers.IntegerField(read_only=True)
    ticket_count = serializers.IntegerField(read_only=True)
    tasks_to_do_count = serializers.IntegerField(read_only=True)
    tasks_high_prio_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Board
        fields = ('id', 'title', 'member_count', 'ticket_count', 
                  'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id')


class BoardDetailSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(source='owner.id', read_only=True)
    members = serializers.SerializerMethodField()
    tasks = serializers.SerializerMethodField()
    
    class Meta:
        model = Board
        fields = ('id', 'title', 'owner_id', 'members', 'tasks')
    
    def get_members(self, obj):
        # Return all members (excluding owner, as owner is separate)
        return UserSerializer(obj.members.all(), many=True).data
    
    def get_tasks(self, obj):
        from tasks_app.api.serializers import TaskListSerializer
        return TaskListSerializer(obj.tasks.all(), many=True).data


class BoardCreateSerializer(serializers.ModelSerializer):
    members = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Board
        fields = ('title', 'members')
    
    def create(self, validated_data):
        members_ids = validated_data.pop('members', [])
        board = Board.objects.create(
            title=validated_data['title'],
            owner=self.context['request'].user
        )
        
        # Add members if provided
        if members_ids:
            members = User.objects.filter(id__in=members_ids)
            board.members.set(members)
        
        return board


class BoardUpdateSerializer(serializers.ModelSerializer):
    members = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    owner_data = UserSerializer(source='owner', read_only=True)
    members_data = serializers.SerializerMethodField()
    
    class Meta:
        model = Board
        fields = ('title', 'members', 'owner_data', 'members_data')
    
    def get_members_data(self, obj):
        return UserSerializer(obj.members.all(), many=True).data
    
    def update(self, instance, validated_data):
        members_ids = validated_data.pop('members', None)
        
        if 'title' in validated_data:
            instance.title = validated_data['title']
        
        if members_ids is not None:
            members = User.objects.filter(id__in=members_ids)
            instance.members.set(members)
        
        instance.save()
        return instance

