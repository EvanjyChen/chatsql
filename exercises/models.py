from django.db import models
from django.contrib.auth.models import User

class DatabaseSchema(models.Model):
    """Three schemas: HR, Ecommerce, School"""
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField()
    db_name = models.CharField(max_length=50)  # practice_hr, practice_ecommerce, practice_school
    schema_sql = models.TextField(help_text="CREATE TABLE statements")
    seed_sql = models.TextField(help_text="INSERT sample data")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name

    class Meta:
        db_table = 'database_schemas'

class Exercise(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    schema = models.ForeignKey(DatabaseSchema, on_delete=models.CASCADE, related_name='exercises')
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    order = models.IntegerField(default=0)
    expected_sql = models.TextField(help_text="Reference solution")
    initial_query = models.TextField(blank=True, help_text="Starter code for students")
    hints = models.JSONField(default=list, help_text='[{"level": 1, "text": "hint1"}, ...]')
    tags = models.JSONField(default=list, help_text='["JOIN", "GROUP BY", "Subquery"]')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.schema.name} - {self.title}"

    class Meta:
        db_table = 'exercises'
        ordering = ['order', 'id']

class UserProgress(models.Model):
    """Track user progress (anonymous via session_id or authenticated via user)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=64, db_index=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    last_query = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_progress'
        unique_together = [['session_id', 'exercise']]

class ChatHistory(models.Model):
    """Store AI chat conversations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=64, db_index=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    response = models.TextField()
    context = models.JSONField(default=dict, help_text='{"query": "...", "error": "..."}')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_history'
        ordering = ['-created_at']

class Submission(models.Model):
    """Track student submissions"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('correct', 'Correct'),
        ('incorrect', 'Incorrect'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='submissions')
    query = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    execution_time = models.FloatField(null=True, blank=True, help_text='Query execution time in seconds')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.exercise.title} - {self.status}"
    
    class Meta:
        db_table = 'submissions'
        ordering = ['-created_at']