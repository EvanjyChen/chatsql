from django.contrib import admin
from .models import DatabaseSchema, Exercise, UserProgress, ChatHistory

@admin.register(DatabaseSchema)
class DatabaseSchemaAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_name', 'db_name', 'created_at']
    search_fields = ['name', 'display_name']

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['title', 'schema', 'difficulty', 'order', 'created_at']
    list_filter = ['schema', 'difficulty']
    search_fields = ['title', 'description']
    ordering = ['order', 'id']

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'exercise', 'completed', 'attempts', 'completed_at']
    list_filter = ['completed', 'exercise__difficulty']
    search_fields = ['session_id']

@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'exercise', 'created_at']
    list_filter = ['created_at']
    search_fields = ['session_id', 'message']
