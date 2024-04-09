import os

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


from HRmanagement_system import settings


class ContractYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    contract_start_year = models.DateField()
    contract_end_year = models.DateField()
    objects = models.Manager()


# Overriding the Default Django Auth User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    user_type_data = ((1, "AdminHr"), (2, "Manager"), (3, "Staff"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class AdminHR(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Manager(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    # def __str__(self):


#     return self.department_name


class Position(models.Model):
    id = models.AutoField(primary_key=True)
    position_name = models.CharField(max_length=255)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, default=1)  # need to give defauult course
    manager_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField()
    address = models.TextField()
    i_d = models.IntegerField(null=True)
    phone = models.IntegerField(null=True)
    department_id = models.ForeignKey(Department, on_delete=models.DO_NOTHING, default=1)
    contract_year_id = models.ForeignKey(ContractYearModel, on_delete=models.SET_DEFAULT, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Attendance(models.Model):
    # Subject Attendance
    id = models.AutoField(primary_key=True)
    position_id = models.ForeignKey(Position, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    contract_year_id = models.ForeignKey(ContractYearModel, on_delete=models.SET_DEFAULT, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class AttendanceReport(models.Model):
    # Individual Student Attendance
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    return_date = models.CharField(max_length=255, default=None)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class LeaveReportManager(models.Model):
    id = models.AutoField(primary_key=True)
    manager_id = models.ForeignKey(Manager, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    return_date = models.CharField(max_length=255, default=None)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class FeedBackManager(models.Model):
    id = models.AutoField(primary_key=True)
    manager_id = models.ForeignKey(Manager, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class NotificationManager(models.Model):
    id = models.AutoField(primary_key=True)
    manager_id = models.ForeignKey(Manager, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class StaffPoint(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    position_id = models.ForeignKey(Position, on_delete=models.CASCADE)
    position_bonus_point = models.FloatField(default=0)
    position_incentive_point = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Contracts(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='media/', default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Policies(models.Model):
    id = models.AutoField(primary_key=True)
    policy_name = models.CharField(max_length=200)
    policy_document = models.FileField(upload_to='media/', default=None)
    objects = models.Manager()

# payroll details
# class Salary(models.Model):
#     id = models.AutoField(primary_key=True)
#     staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     date = models.DateField()
#
#
# class Benefits(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#
#
# class Deduction(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#
#
# class Payroll(models.Model):
#     id = models.AutoField(primary_key=True)
#     staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
#     salary = models.OneToOneField(Salary, on_delete=models.CASCADE)
#     benefits = models.ManyToManyField(Benefits, blank=True)
#

# Creating Django Signals

# It's like trigger in database. It will run only when Data is Added in CustomUser model

@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HR, Manager or Staff
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            AdminHR.objects.create(admin=instance)
        if instance.user_type == 2:
            Manager.objects.create(admin=instance)
        if instance.user_type == 3:
            Staff.objects.create(admin=instance, department_id=Department.objects.get(id=1),
                                 contract_year_id=ContractYearModel.objects.get(id=1), address="", profile_pic="",
                                 gender="")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhr.save()
    if instance.user_type == 2:
        instance.manager.save()
    if instance.user_type == 3:
        instance.staff.save()
