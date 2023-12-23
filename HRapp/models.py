from django.db import models
from django.utils import timezone

class Employees(models.Model):
    employeeID = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phoneNumber = models.IntegerField(default=0)
    address = models.CharField(max_length=255)
    dateOB = models.DateTimeField()
    jobTitle = models.CharField(max_length=255)
    dateOfHire = models.DateTimeField()
    salary = models.IntegerField(default=0)
    bankaccNo = models.IntegerField(default=0)
    taxExemption = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"

class OnBoarding(models.Model):
    onboardingID = models.AutoField(primary_key=True)
    employeeID = models.ForeignKey(Employees, null=True, blank=True, on_delete=models.SET_NULL, related_name='employee_onboarding_set')
    jobTitleReference = models.ForeignKey(Employees, null=True, blank=True, on_delete=models.SET_NULL, related_name='jobtitle_onboarding_set')
    jobDescription = models.TextField()
    salaryRange = models.IntegerField(default=0)

    def __str__(self):
        return str(self.onboardingID)

class Performance(models.Model):
    reviewID = models.AutoField(primary_key=True)
    employeeID = models.ForeignKey(Employees, null=True, blank=True, on_delete=models.SET_NULL)
    reviewDate = models.DateTimeField()
    reviewer = models.CharField(max_length=255)
    performanceScore = models.IntegerField(default=0)
    comment = models.TextField()

    def __str__(self):
        return str(self.reviewID)

class Attendance(models.Model):
    attendanceID = models.AutoField(primary_key=True)
    employeeID = models.ForeignKey(Employees, null=True, blank=True, on_delete=models.SET_NULL)
    clockIn = models.DateTimeField()
    clockOut = models.DateTimeField()

    def __str__(self):
        return str(self.attendanceID)

class Payroll(models.Model):
    payrollID = models.AutoField(primary_key=True)
    employeeID = models.ForeignKey(Employees, null=True, blank=True, on_delete=models.SET_NULL)
    payrollStartDate = models.DateTimeField()
    payrollEndDate = models.DateTimeField()
    regularHours = models.DecimalField(max_digits=5, decimal_places=2)
    overtimeHours = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.payrollID)

class LeaveRequest(models.Model):
    requestID = models.AutoField(primary_key=True)
    employeeID = models.ForeignKey(Employees, null=True, blank=True, on_delete=models.SET_NULL)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    reason = models.TextField()
    status = models.BooleanField(default=False)  # False: Pending / True:

    def __str__(self):
        return str(self.requestID)

class Benefits(models.Model):
    benefitID = models.AutoField(primary_key=True)
    employeeID = models.ForeignKey(Employees, null=True, blank=True, on_delete=models.SET_NULL)
    benefitName = models.CharField(max_length=255)
    typeOfBenefit = models.CharField(max_length=100)
    benefitDescription = models.TextField()
    benefitStartDate = models.DateTimeField()
    benefitEndDate = models.DateTimeField()

    def __str__(self):
        return str(self.benefitID)

class CompliancePolicy(models.Model):
    policyID = models.AutoField(primary_key=True)
    policyName = models.CharField(max_length=255)
    policyDescription = models.TextField()
    acknowledgementDate = models.DateTimeField()

    def __str__(self):
        return str(self.policyID)
