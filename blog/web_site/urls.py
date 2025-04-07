from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('categories/<str:category_id>/', views.category_articles,
         name='category_articles'),
]
