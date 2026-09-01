from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from portprofile import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('edit/', views.edit_portfolio, name='edit'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Skills
    path('edit/skill/add/', views.add_skill, name='add_skill'),
    path('edit/skill/<int:pk>/', views.edit_skill, name='edit_skill'),
    path('edit/skill/<int:pk>/delete/', views.delete_skill, name='delete_skill'),

    # Projects
    path('edit/project/add/', views.add_project, name='add_project'),
    path('edit/project/<int:pk>/', views.edit_project, name='edit_project'),
    path('edit/project/<int:pk>/delete/', views.delete_project, name='delete_project'),

    # Experience
    path('edit/experience/add/', views.add_experience, name='add_experience'),
    path('edit/experience/<int:pk>/', views.edit_experience, name='edit_experience'),
    path('edit/experience/<int:pk>/delete/', views.delete_experience, name='delete_experience'),
    path('contact/', views.contact, name='contact'),
]