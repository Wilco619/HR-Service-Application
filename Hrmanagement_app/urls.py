
from django.urls import path, include
from . import views
from .import HrViews, ManagerViews, StaffViews


urlpatterns = [
    path('', views.loginPage, name="login"),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('get_user_details/', views.get_user_details, name="get_user_details"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('admin_home/', HrViews.admin_home, name="admin_home"),

    path('add_manager/', HrViews.add_manager, name="add_manager"),
    path('add_manager_save/', HrViews.add_manager_save, name="add_manager_save"),
    path('manage_manager/', HrViews.manage_manager, name="manage_manager"),
    path('edit_manager/<manager_id>/', HrViews.edit_manager, name="edit_manager"),
    path('edit_manager_save/', HrViews.edit_manager_save, name="edit_manager_save"),
    path('delete_manager/<manager_id>/', HrViews.delete_manager, name="delete_manager"),

    path('add_department/', HrViews.add_department, name="add_department"),
    path('add_department_save/', HrViews.add_department_save, name="add_department_save"),
    path('manage_department/', HrViews.manage_department, name="manage_department"),
    path('edit_department/<department_id>/', HrViews.edit_department, name="edit_department"),
    path('edit_department_save/', HrViews.edit_department_save, name="edit_department_save"),
    path('delete_department/<department_id>/', HrViews.delete_department, name="delete_department"),

    path('manage_contract/', HrViews.manage_contract, name="manage_contract"),
    path('add_contract/', HrViews.add_contract, name="add_contract"),
    path('add_contract_save/', HrViews.add_contract_save, name="add_contract_save"),
    path('edit_contract/<contract_id>', HrViews.edit_contract, name="edit_contract"),
    path('edit_contract_save/', HrViews.edit_contract_save, name="edit_contract_save"),
    path('delete_contract/<contract_id>/', HrViews.delete_contract, name="delete_contract"),

    path('add_staff/', HrViews.add_staff, name="add_staff"),
    path('add_staff_save/', HrViews.add_staff_save, name="add_staff_save"),
    path('edit_staff/<staff_id>', HrViews.edit_staff, name="edit_staff"),
    path('edit_staff_save/', HrViews.edit_staff_save, name="edit_staff_save"),
    path('manage_staff/', HrViews.manage_staff, name="manage_staff"),
    path('delete_staff/<staff_id>/', HrViews.delete_staff, name="delete_staff"),

    path('add_position/', HrViews.add_position, name="add_position"),
    path('add_position_save/', HrViews.add_position_save, name="add_position_save"),
    path('manage_position/', HrViews.manage_position, name="manage_position"),
    path('edit_position/<position_id>/', HrViews.edit_position, name="edit_position"),
    path('edit_position_save/', HrViews.edit_position_save, name="edit_position_save"),
    path('delete_position/<position_id>/', HrViews.delete_position, name="delete_position"),

    path('check_email_exist/', HrViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist/', HrViews.check_username_exist, name="check_username_exist"),

    path('staff_feedback_message/', HrViews.staff_feedback_message, name="staff_feedback_message"),
    path('staff_feedback_message_reply/', HrViews.staff_feedback_message_reply, name="staff_feedback_message_reply"),

    path('manager_feedback_message/', HrViews.manager_feedback_message, name="manager_feedback_message"),
    path('manager_feedback_message_reply/', HrViews.manager_feedback_message_reply, name="manager_feedback_message_reply"),

    path('staff_leave_view/', HrViews.staff_leave_view, name="staff_leave_view"),
    path('staff_leave_approve/<leave_id>/', HrViews.staff_leave_approve, name="staff_leave_approve"),
    path('staff_leave_reject/<leave_id>/', HrViews.staff_leave_reject, name="staff_leave_reject"),
    path('staff_contract/', HrViews.staff_contract, name="staff_contract"),
    path('staff_contract_upload/<int:staff_id>/', HrViews.staff_contract_upload, name="staff_contract_upload"),
    path('staff_contract_save/', HrViews.staff_contract_save, name="staff_contract_save"),

    path('manager_leave_view/', HrViews.manager_leave_view, name="manager_leave_view"),
    path('manager_leave_approve/<leave_id>/', HrViews.manager_leave_approve, name="manager_leave_approve"),
    path('manager_leave_reject/<leave_id>/', HrViews.manager_leave_reject, name="manager_leave_reject"),

    path('admin_view_attendance/', HrViews.admin_view_attendance, name="admin_view_attendance"),
    path('admin_get_attendance_dates/', HrViews.admin_get_attendance_dates, name="admin_get_attendance_dates"),
    path('admin_get_attendance_staff/', HrViews.admin_get_attendance_staff, name="admin_get_attendance_staff"),

    path('admin_profile/', HrViews.admin_profile, name="admin_profile"),
    path('policies/', HrViews.policies, name="policies"),
    path('upload_policy/', HrViews.upload_policy, name="upload_policy"),
    path('admin_profile_update/', HrViews.admin_profile_update, name="admin_profile_update"),
    

    
    # URLS for Manager
    path('manager_home/', ManagerViews.manager_home, name="manager_home"),
    path('manager_take_attendance/', ManagerViews.manager_take_attendance, name="manager_take_attendance"),
    path('get_staffs/', ManagerViews.get_staffs, name="get_staffs"),

    path('save_attendance_data/', ManagerViews.save_attendance_data, name="save_attendance_data"),
    path('manager_update_attendance/', ManagerViews.manager_update_attendance, name="manager_update_attendance"),
    path('get_attendance_dates/', ManagerViews.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_staff/', ManagerViews.get_attendance_staff, name="get_attendance_staff"),
    path('update_attendance_data/', ManagerViews.update_attendance_data, name="update_attendance_data"),
    path('manager_apply_leave/', ManagerViews.manager_apply_leave, name="manager_apply_leave"),
    path('manager_apply_leave_save/', ManagerViews.manager_apply_leave_save, name="manager_apply_leave_save"),
    path('manager_feedback/', ManagerViews.manager_feedback, name="manager_feedback"),
    path('manager_feedback_save/', ManagerViews.manager_feedback_save, name="manager_feedback_save"),
    path('manager_profile/', ManagerViews.manager_profile, name="manager_profile"),
    path('manager_profile_update/', ManagerViews.manager_profile_update, name="manager_profile_update"),
    path('manager_add_result/', ManagerViews.manager_add_result, name="manager_add_result"),
    path('manager_add_result_save/', ManagerViews.manager_add_result_save, name="manager_add_result_save"),

    # URLS for Staff
    path('staff_home/', StaffViews.staff_home, name="staff_home"),
    path('staff_view_attendance/', StaffViews.staff_view_attendance, name="staff_view_attendance"),
    path('staff_view_attendance_post/', StaffViews.staff_view_attendance_post, name="staff_view_attendance_post"),
    path('staff_apply_leave/', StaffViews.staff_apply_leave, name="staff_apply_leave"),
    path('staff_apply_leave_save/', StaffViews.staff_apply_leave_save, name="staff_apply_leave_save"),
    path('staff_feedback/', StaffViews.staff_feedback, name="staff_feedback"),
    path('staff_feedback_save/', StaffViews.staff_feedback_save, name="staff_feedback_save"),
    path('staff_profile/', StaffViews.staff_profile, name="staff_profile"),
    path('staff_profile_update/', StaffViews.staff_profile_update, name="staff_profile_update"),
    path('staff_view_result/', StaffViews.staff_view_result, name="staff_view_result"),
    path('view_staff_contract/', StaffViews.view_staff_contract, name="view_staff_contract"),
    path('view_policy/', StaffViews.view_policy, name="view_policy"),
]
