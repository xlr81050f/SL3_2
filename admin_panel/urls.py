from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.AdminDashboardView.as_view(), name='dashboard'),
    path('shows/', views.ShowListAdminView.as_view(), name='show_list'),
    path('shows/create/', views.ShowCreateView.as_view(), name='show_create'),
    path('shows/<int:pk>/', views.ShowDetailAdminView.as_view(), name='show_detail'),
    path('shows/<int:pk>/update/', views.ShowUpdateView.as_view(), name='show_update'),
    path('shows/<int:pk>/delete/', views.ShowDeleteView.as_view(), name='show_delete'),
    path('shows/<int:show_id>/showtimes/create/', views.ShowtimeCreateView.as_view(), name='showtime_create'),
    path('bookings/', views.BookingListAdminView.as_view(), name='booking_list'),
    path('bookings/<int:pk>/', views.BookingDetailAdminView.as_view(), name='booking_detail'),
]