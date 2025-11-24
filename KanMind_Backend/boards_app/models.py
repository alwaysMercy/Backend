from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Board(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_boards')
    members = models.ManyToManyField(User, related_name='member_boards', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    @property
    def member_count(self):
        return self.members.count() + 1  # +1 for owner
    
    @property
    def ticket_count(self):
        return self.tasks.count()
    
    @property
    def tasks_to_do_count(self):
        return self.tasks.filter(status='to-do').count()
    
    @property
    def tasks_high_prio_count(self):
        return self.tasks.filter(priority='high').count()

