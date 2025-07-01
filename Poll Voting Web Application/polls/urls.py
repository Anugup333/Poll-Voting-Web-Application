from django.urls import path
from . import views

urlpatterns = [
    
    # --- Admin URLs ---
    path('polls/admin/', views.admin_poll_list, name='admin_poll_list'),
    path('polls/create/', views.create_poll, name='create_poll'),
    path('polls/<int:poll_id>/edit/', views.edit_poll, name='edit_poll'),
    path('polls/<int:poll_id>/delete/', views.delete_poll, name='delete_poll'),
    path('polls/<int:poll_id>/results_admin/', views.poll_results_admin, name='poll_results_admin'),

    # --- User URLs ---
    path('polls/', views.poll_list, name='poll_list'),
    path('polls/<int:poll_id>/vote/', views.vote_poll, name='vote_poll'),
    path('polls/<int:poll_id>/results_user/', views.poll_results_user, name='poll_results_user'),
]
