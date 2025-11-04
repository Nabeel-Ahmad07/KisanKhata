from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('market/', views.market, name='market'),
    path('weather/', views.weather, name='weather'),

    #Admin
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-item/', views.add_item, name='add_item'),
    path('edit-item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('delete-item/<int:item_id>/', views.delete_item, name='delete_item'),

    #Farmer
    path('farmer_dashboard/', views.farmer_dashboard, name='farmer_dashboard'),

    #Forum
    path('forum/', views.forum_home, name='forum_home'),
    path('forum/new/', views.create_post, name='create_post'),
    path('forum/<int:post_id>/', views.post_detail, name='post_detail'),
    path('forum/<int:post_id>/delete/', views.delete_post, name='delete_post'),
]