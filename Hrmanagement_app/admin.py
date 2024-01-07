from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, AdminHR, Manager, Department, Position, Staff, Attendance, AttendanceReport, LeaveReportStaff, LeaveReportManager, FeedBackStaff, FeedBackManager, NotificationStaff, NotificationManager

# Register your models here.
class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)

admin.site.register(AdminHR)
admin.site.register(Manager)
admin.site.register(Department)
admin.site.register(Position)
admin.site.register(Staff)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)
admin.site.register(LeaveReportStaff)
admin.site.register(LeaveReportManager)
admin.site.register(FeedBackStaff)
admin.site.register(FeedBackManager)
admin.site.register(NotificationStaff)
admin.site.register(NotificationManager)
