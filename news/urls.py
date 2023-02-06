from django.urls import path
from . import views


app_name = 'news'
urlpatterns = [
    path('', views.MainPage.as_view()),
    path('news/<int:article_id>/', views.Article.as_view()),
    path('news/', views.NewsPage.as_view()),
    path('news/create/', views.CreateNews.as_view()),
]