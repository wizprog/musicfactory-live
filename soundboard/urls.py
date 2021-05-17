from django.urls import include, path
from soundboard import views

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]

urlpatterns += [
    path('tracks/', views.TrackListView.as_view(), name='track-list'),
    path('tracks/create/', views.TrackCreateView.as_view(), name='track-create'),
    path('tracks/<int:pk>/', views.TrackDetailView.as_view(), name='track-detail'),
    path('tracks/update/<int:pk>/', views.TrackUpdateView.as_view(), name='track-update'),
    path('tracks/delete/<int:pk>/', views.TrackDeleteView.as_view(), name='track-delete'),
    path('tracks/<int:track_id>/calculate-start-time/', views.calculate_start_time, name='track-start-time'),
    path('media/<str:track_name>', views.download_song),
]