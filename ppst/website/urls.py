from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('submit_ticket/', views.submit_ticket, name='submit_ticket'),
    path('get_user_tickets/', views.get_user_tickets, name='get_user_tickets'),
    path('create_test/', views.create_test, name='create_test'),  # Create test endpoint
    path('testpage/<str:link>/', views.test_page_view, name='testpage'),  # New URL for taking the test
    path('get_test_results/', views.get_test_results, name='get_test_results'),  # Get user's tests results
    path('test_results/<int:test_id>/', views.test_results, name='test_results'),  # Specific test results
]
