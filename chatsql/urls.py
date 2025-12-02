from django.contrib import admin
from django.urls import path, include
from exercises.views import (
    SchemaListView,
    ExerciseListView,
    ExerciseDetailView,
    ExecuteQueryView,
    SubmitQueryView
)
from ai_tutor.views import ExerciseAIView
from frontend.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schemas/', SchemaListView.as_view(), name='schema-list'),
    path('api/exercises/', ExerciseListView.as_view(), name='exercise-list'),
    path('api/exercises/<int:exercise_id>/', ExerciseDetailView.as_view(), name='exercise-detail'),
    path('api/exercises/<int:exercise_id>/execute/', ExecuteQueryView.as_view(), name='execute-query'),
    path('api/exercises/<int:exercise_id>/submit/', SubmitQueryView.as_view(), name='submit-query'),
    path('api/exercises/<int:exercise_id>/ai/', ExerciseAIView.as_view(), name='exercise-ai'),
    path('', IndexView.as_view(), name='index'),
    path('api/auth/', include('accounts.urls')),
    path('', include('frontend.urls')),
]
