"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views
from django.views.generic import RedirectView
from iceberg_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/register', permanent=True)),
    path('register/', RegisterView.as_view(), name='register'),
    path('home/', home_view, name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('create_workspace/', WorkspaceCreationView.as_view(), name='create_workspace'),
    path('workspace/<int:id>', workspace_view, name='workspace'),
    path('create_board/<int:id>', create_board_view, name='create_board'),
    path('delete_workspace/<int:id>', delete_workspace_view, name='delete_workspace'),
    path('delete_board/<int:board_id>/<int:workspace_id>', delete_board_view, name='delete_board'),
    path('create_task/<int:board_id>/<int:workspace_id>', create_task_view, name='create_task'),
    path('task_info/<int:task_id>/<int:workspace_id>', task_info_view, name='task_info'),
    path('logout/', logout_view, name='logout'),
    path('invite_creation/<int:workspace_id>', invite_creation_view, name='invite_creation'),
    path('delete_task/<int:task_id>/<int:workspace_id>', delete_task_view, name='delete_task'),
]
