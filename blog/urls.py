from django.urls import path
from . import views
from .feeds import LatestPostsFeed  # Import the RSS feed

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',  
         views.post_detail,
         name='post_detail'),
    
    path('<int:post_id>/share/', views.post_share, name='post_share'),

    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),

    # RSS feed URL pattern
    path('feed/', LatestPostsFeed(), name='post_feed'),
]
