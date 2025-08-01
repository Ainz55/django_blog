from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('categories/<str:category_id>/', views.category_articles,
         name='category_articles'),
    path('articles/<str:article_id>/', views.article_detail,
         name="article_detail"),
    path('login/', views.login_view, name="login"),
    path('registration/', views.registration_view, name="registration"),
    path('logout/', views.user_logout, name='logout'),
    path('article/create/', views.create_article, name='create'),
    path('article/delete/<str:pk>/', views.ArticleDeleteView.as_view(),
         name='delete'),
    path('article/update/<str:pk>/', views.ArticleUpdateView.as_view(), name='update'),

    path('profile/<str:username>/', views.profile_view, name='profile'),

    path('<str:obj_type>/<int:obj_id>/<str:action>/', views.add_like_or_dislike, name='add_vote')
]
