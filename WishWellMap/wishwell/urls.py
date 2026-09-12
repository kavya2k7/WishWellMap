from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('shelves/', views.shelf_list, name='shelf_list'),
    path('items/', views.bucket_item_list, name='bucket_item_list'),
    path('items/add/', views.add_bucket_item, name='add_bucket_item'),
    path('items/<int:pk>/edit/', views.edit_bucket_item, name='edit_bucket_item'),
    path('items/<int:pk>/delete/', views.delete_bucket_item, name='delete_bucket_item'),
    path('items/<int:item_id>/add-memory/', views.add_memory, name='add_memory'),
    path('memories/', views.memories_album, name='memories_album'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('api/calendar-events/', views.calendar_events_api, name='calendar_events_api'),  
    path('items/<int:pk>/edit/', views.edit_bucket_item, name='edit_bucket_item'),
    path('shelves/edit/<int:pk>/', views.edit_shelf, name='edit_shelf'),
]



