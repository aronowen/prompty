from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('team/', views.team, name = 'team'),
    path('role/hr-manager/', views.hr, name = 'hr'),
    path('role/data-analyst/', views.da, name = 'da'),
    path('role/marketing-strategist/', views.ms, name = 'ms'),
    path('role/product-designer/', views.pd, name = 'pd'),
    path('role/customer-support/', views.cs, name = 'cs'),
    path('role/copywriter/', views.cw, name = 'cw'),
    path('role/it-specialist/', views.it, name = 'it'),
    path('role/random/', views.random_role, name='random'),
    path("leaderboard/", views.leaderboard, name="leaderboard"),
    path("result/<int:pk>/", views.result, name="result"),
    path('robots.txt', TemplateView.as_view(template_name="home/robots.txt", content_type="text/plain"))
]