from django.urls import path
from . import views

urlpatterns = [
    path('',  views.post_list, name='post_list'),
    path('create/', views.create_post, name='create_post'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('category/<slug:category_slug>/', views.category_detail, name='category_detail'),
    path('post/<slug:slug>/edit/', views.edit_post, name='edit_post'), # URL for category filtering
    path('post/<slug:slug>/delete/', views.delete_post, name='delete_post'),
    #path('post/<int:pk>/like_unlike/', views.like_unlike_post, name='like_unlike_post'),
     
]