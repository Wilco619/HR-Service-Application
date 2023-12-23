from django.contrib import admin
from . models import Employees, OnBoarding, Performance, Payroll, Attendance, LeaveRequest, Benefits, CompliancePolicy

# Register your models here.
@admin.register(Employees)
class EmployeesModelAdmin(admin.ModelAdmin):
    list_display = ['employeeID','firstName','email','phoneNumber','jobTitle','dateOfHire','salary','bankaccNo','taxExemption']

@admin.register(OnBoarding)
class OnboardingModelAdmin(admin.ModelAdmin):
    list_display = ['onboardingID','employeeID','jobTitleReference','jobDescription','salaryRange']

@admin.register(Performance)
class PerformanceModelAdmin(admin.ModelAdmin):
    list_display = ['reviewID','employeeID','reviewDate','reviewer','performanceScore','comment']

@admin.register(Attendance)
class AttendanceModelAdmin(admin.ModelAdmin):
    list_display = ['attendanceID','employeeID','clockIn','clockOut']

@admin.register(Payroll)
class PayrollModelAdmin(admin.ModelAdmin):
    list_display = ['payrollID','employeeID','payrollStartDate','payrollEndDate','regularHours','overtimeHours']

@admin.register(LeaveRequest)
class LeaveRequestModelAdmin(admin.ModelAdmin):
    list_display = ['requestID','employeeID','startDate','endDate','reason','status']

@admin.register(Benefits)
class BenefitsModelAdmin(admin.ModelAdmin):
    list_display = ['benefitID','employeeID','benefitName','typeOfBenefit','benefitDescription','benefitStartDate','benefitEndDate']

@admin.register(CompliancePolicy)
class CompliancePolicyModelAdmin(admin.ModelAdmin):
    list_display = ['policyID','policyName','policyDescription','acknowledgementDate']