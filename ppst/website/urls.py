from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.home, name='home'),
    path('admin/logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('submit-response/', views.submit_response, name='submit_response'),
    path('get-stimuli/', views.get_stimuli, name='get_stimuli'),
    path('submit_ticket/', views.submit_ticket, name='submit_ticket'),
    path('get_user_tickets/', views.get_user_tickets, name='get_user_tickets'),
    path('admin_tickets/', views.admin_view_tickets, name='admin_tickets'),
    path('update_ticket_status/<int:ticket_id>/', views.update_ticket_status, name='update_ticket_status'),
    path('complete_ticket/<int:ticket_id>/', views.complete_ticket, name='complete_ticket'),
    path('create_test/', views.create_test, name='create_test'),  # Create test endpoint
    path('delete_test/<int:test_id>/', views.delete_invalid_test, name='delete_invalid_test'),
    path('testpage/<str:link>/', views.test_page_view, name='testpage'),  # New URL for taking the test
    path('get_test_results/<str:test_status>/', views.get_test_results, name='get_test_results'),  # Get user's tests results
    path('test_results/<int:test_id>/', views.test_results, name='test_results'),  # Specific test results
    path('update_account/', views.update_account, name='update_account'),
    path('get_user_info/', views.get_user_info, name='get_user_info'),
    path('get_user_notifications/<str:load_type>/', views.get_user_notifications, name='get_user_notifications'),
    path('dismiss_notification/<int:id>/', views.dismiss_notification, name='dismiss_notification'),
    path('mark_as_read/<int:id>/', views.mark_as_read, name='mark_as_read'),
    path('dismiss_notification/<int:id>/', views.dismiss_notification, name='dismiss_notification'),
    path('check-test-status/<str:link>/', views.check_test_status, name='check-test-status'),
    path('start-test/<str:link>/', views.start_test, name='start_test'),
    path('mark-test-complete/<str:link>/', views.mark_test_complete, name='mark_test_complete'),
    path('invalidate_test/<str:link>/', views.invalidate_test, name='invalidate_test'),
    path('errorpage/', views.errorpage, name="errorpage"),
    path('get_test_comparison_data/<int:test_id>/', views.get_test_comparison_data, name='get_test_comparison_data'),
    path('completed/', views.completionpage, name="completionpage"),
    path('get_registration_requests/', views.get_registration_requests, name='get_registration_requests'),
    path('approve_registration/<int:registration_id>/', views.approve_registration, name='approve_registration'),
    path('deny_registration/<int:registration_id>/', views.deny_registration, name='deny_registration'),
    path('create_result_charts/<int:test_id>/', views.create_result_charts, name='create_result_charts'),

]
