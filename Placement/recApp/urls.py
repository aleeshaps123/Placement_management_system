from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import submit_placement, admin_review_placements, approve_placement, reject_placement, placement_details

urlpatterns = [
    path('',views.home,name="home"),
    path('aboutus',views.aboutus,name='aboutus'),
    path('contact',views.contact_view,name='contact'),
    path('pdashboard/',views.coordinator_dashboard,name="coordinator"),
    path('addcompany',views.add_company,name='addcompany'),
    path('displaycompany',views.display_company,name='displaycompany'),
    path('addplacement',views.add_placement,name='addplacement'),
    path('displayplacement',views.display_placements,name='displayplacement'),
    path('displayplacement/<int:placement_id>/applicants/',views.view_applicants, name='view_applicants'),

    path('student',views.student_dashboard,name='student_dashboard'),
    path('signup',views.studentsignup,name='signup'),
    path('login/', views.student_login, name='student_login'),
    path('updateprofile/', views.update_profile, name='updateprofile'),
    path('student/placements/', views.student_placements, name='studentplacements'),
    path('student/apply/<int:placement_id>/', views.apply_for_placement, name='apply_for_placement'),
    # URL for viewing applied placements
    path('applied_placements/', views.applied_placements, name='applied_placements'),

    # URL for canceling the application
    path('cancel_application/<int:application_id>/', views.cancel_application, name='cancel_application'),
    path('student_profiles/', views.student_profiles, name='student_profiles'),
    path('export_filtered_applicants_to_excel/<int:placement_id>/', views.export_filtered_applicants_to_excel, name='export_filtered_applicants_to_excel'),
    path('add_placed_student/', views.add_placed_student, name='add_placed_student'),
    path('display_placed_students/', views.display_placed_students, name='display_placed_students'),
    path('placements_by_year',views.placements_by_year, name='placements_by_year'),
    path('get_chart_data/', views.get_chart_data, name='get_chart_data'),
    path('delete-company/<int:company_id>/', views.delete_company, name='delete_company'),
    path('logout/', views.student_logout, name='logout'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
    path('student-summary/', views.department_statistics, name='department_statistics'),
    path("submit-placement/", views.submit_placement, name="submit_placement"),
    path("placement-status/", views.student_placement_status, name="student_placement_status"),

    # Admin URLs
    path("review-placements/", views.admin_review_placements, name="admin_review_placements"),
    path("approve-placement/<int:placement_id>/", views.approve_placement, name="approve_placement"),
    path("reject-placement/<int:placement_id>/", views.reject_placement, name="reject_placement"),
    path('placement/<int:placement_id>/', placement_details, name='placement_details'),

    ]