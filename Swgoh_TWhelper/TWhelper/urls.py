
from django.urls import path, re_path
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views
from .views import (
    TeamListView,
    TeamDetailView,
    TeamCreateView,
    TeamUpdateView,
    TeamDeleteView,
    TeamsViewSet,
    TeamsPostView,
)
from . import views
# from .views import background_view


urlpatterns = [
    path('', views.home, name='TWhelper-home'),
    path('teste/', views.teste, name='TWhelper-teste'),
    path('teams/', views.teams, name='TWhelper-teams'),
    path('teams_edit/', TeamListView.as_view(), name='TWhelper-editteams'),
    path('teams_edit/new/', TeamCreateView.as_view(), name='TWhelper-teamscreate'),
    path('teams_edit/<pk>/update', TeamUpdateView.as_view(template_name='TWhelper/teams_edit_team.html'),
         name='TWhelper-teamsupdate'),
    path('teams_edit/<pk>/delete', TeamDeleteView.as_view(), name='TWhelper-teamsdelete'),
    path('mandalorians/', views.mandalorians, name='TWhelper-mandalorians'),
    path('teamsapi/', TeamsViewSet.as_view(), name='teams-api'),
    path('teamsapi/<pk>/', csrf_exempt(TeamsPostView.as_view()), name='teams-rud'),
    path('mandalorians/json/', views.mandalorians_json, name='TWhelper-mandalorians_json'),
    path('v1/tasks/', views.tasks, name='tasks'),
    path('login/', auth_views.LoginView.as_view(template_name='TWhelper/home.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='TWhelper/home.html'), name='logout'),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^export/xls/$', views.export_teams_xls, name='export_teams_xls'),
    # surl(r'^/', background_view, name='background_view'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
