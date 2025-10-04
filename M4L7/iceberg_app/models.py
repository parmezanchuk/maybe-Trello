from django.db import models
from django.contrib.auth.models import User


class WorkSpace(models.Model):
    name = models.CharField(max_length=50)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_workspaces')

    members = models.ManyToManyField(User, related_name='member_workspaces')

    def __str__(self):
        return f'{self.name}, owner - {self.owner}'
class Board(models.Model):
    name = models.CharField(max_length=25)

    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Task(models.Model):
    IMPORTANCE_CHOICES = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
    ]

    DIFFICULTY_CHOICES = [
        (1, 'trivially'),
        (2, 'easy'),
        (3, 'medium'),
        (4, 'hard'),
        (5, 'very hard'),
    ]

    STATUS_CHOICES = [
        ('awaits', 'awaits'),
        ('in progress', 'in progress'),
        ('completed', 'completed'),
        ('failed', 'failed'),
    ]

    title = models.CharField(max_length=25)
    description = models.CharField(max_length=500)
    importance = models.IntegerField(choices=IMPORTANCE_CHOICES)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='tasks')


    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment in {self.created_at}, author - {self.author}"

class UserInvite(models.Model):
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')

    created_at = models.DateTimeField(auto_now_add=True)
