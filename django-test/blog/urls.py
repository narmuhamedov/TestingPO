from django.urls import path
from . import views

urlpatterns = [
    path('blog_list/', views.blog_list_view, name='blog_list'),
    path('blog_list/<int:id>/', views.blog_detail_view, name='blog_detail'),
    path('create_blog/', views.create_blog_view, name='create_blog'),
    path('blog_list/<int:id>/update/', views.update_blog, name='update_blog'),
    path('blog_list/<int:id>/delete/', views.delete_blog_view, name='delete_blog')
]