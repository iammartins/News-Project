from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.analysis_dashboard, name='analysis_dashboard'),
    path('track_site_visit/', views.track_site_visit, name='track_site_visit'),
    path('track_post_view/<int:pk>/', views.track_post_view, name='track_post_view'),  # Add <int:pk> for post ID
    path('track_category_read/<int:pk>/', views.track_category_read, name='track_category_read'), # Add <int:pk> for category ID
]