from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    
    path('create-teams/', views.create_teams, name='create_teams'),
    path('queue/<uuid:admin_input_id>/', views.join_queue, name='join_queue'),
    path('teams/<uuid:admin_input_id>/', views.get_team_assignments, name='get_team_assignments'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)