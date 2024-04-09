from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
import datetime  # To Parse input DateTime into Python Date Time Object

from Hrmanagement_app.models import CustomUser, Staff, Department, Position, Staff, Attendance, AttendanceReport, \
    LeaveReportStaff, FeedBackStaff, StaffPoint, Contracts, Policies


def staff_home(request):
    staff_obj = Staff.objects.get(admin=request.user.id)
    total_attendance = AttendanceReport.objects.filter(staff_id=staff_obj).count()
    attendance_present = AttendanceReport.objects.filter(staff_id=staff_obj, status=True).count()
    attendance_absent = AttendanceReport.objects.filter(staff_id=staff_obj, status=False).count()

    department_obj = Department.objects.get(id=staff_obj.department_id.id)
    total_positions = Position.objects.filter(department_id=department_obj).count()

    position_name = []
    data_present = []
    data_absent = []
    position_data = Position.objects.filter(department_id=staff_obj.department_id)
    for position in position_data:
        attendance = Attendance.objects.filter(position_id=position.id)
        attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True,
                                                                   staff_id=staff_obj.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=False,
                                                                  staff_id=staff_obj.id).count()
        position_name.append(position.position_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)

    context = {
        "total_attendance": total_attendance,
        "attendance_present": attendance_present,
        "attendance_absent": attendance_absent,
        "total_positions": total_positions,
        "position_name": position_name,
        "data_present": data_present,
        "data_absent": data_absent
    }
    return render(request, "staff_template/staff_home_template.html", context)


def staff_view_attendance(request):
    staff = Staff.objects.get(admin=request.user.id)  # Getting Logged in Staff Data
    department = staff.department_id  # Getting Department Enrolled of LoggedIn Staff
    # department = Department.objects.get(id=staff.department_id.id) # Getting Department Enrolled of LoggedIn Staff
    positions = Position.objects.filter(department_id=department)  # Getting the Positions of Department Enrolled
    context = {
        "positions": positions
    }
    return render(request, "staff_template/staff_view_attendance.html", context)


def staff_view_attendance_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_view_attendance')
    else:
        # Getting all the Input Data
        position_id = request.POST.get('position')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Parsing the date data into Python object
        start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        # Getting all the Positions Data based on Selected Position
        position_obj = Position.objects.get(id=position_id)
        # Getting Logged In User Data
        user_obj = CustomUser.objects.get(id=request.user.id)
        # Getting Staff Data Based on Logged in Data
        stuf_obj = Staff.objects.get(admin=user_obj)

        # Now Accessing Attendance Data based on the Range of Date Selected and Position Selected
        attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse, end_date_parse),
                                               position_id=position_obj)
        # Getting Attendance Report based on the attendance details obtained above
        attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance, staff_id=stuf_obj)

        # for attendance_report in attendance_reports:
        #     print("Date: "+ str(attendance_report.attendance_id.attendance_date), "Status: "+ str(attendance_report.status))

        # messages.success(request, "Attendacne View Success")

        context = {
            "position_obj": position_obj,
            "attendance_reports": attendance_reports
        }

        return render(request, 'staff_template/staff_attendance_data.html', context)


def staff_apply_leave(request):
    staff_obj = Staff.objects.get(admin=request.user.id)
    leave_data = LeaveReportStaff.objects.filter(staff_id=staff_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, 'staff_template/staff_apply_leave.html', context)


def staff_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('staff_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        return_date = request.POST.get('return_date')
        leave_message = request.POST.get('leave_message')

        staff_obj = Staff.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStaff(staff_id=staff_obj, leave_date=leave_date, return_date=return_date, leave_message=leave_message,
                                            leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('staff_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('staff_apply_leave')


def staff_feedback(request):
    staff_obj = Staff.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaff.objects.filter(staff_id=staff_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'staff_template/staff_feedback.html', context)


def staff_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('staff_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        staff_obj = Staff.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStaff(staff_id=staff_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('staff_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('staff_feedback')


def staff_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staff.objects.get(admin=user)

    context = {
        "user": user,
        "staff": staff
    }
    return render(request, 'staff_template/staff_profile.html', context)


def staff_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('staff_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            staff = Staff.objects.get(admin=customuser.id)
            staff.address = address
            staff.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('staff_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('staff_profile')


def staff_view_result(request):
    staff = Staff.objects.get(admin=request.user.id)
    staff_result = StaffPoint.objects.filter(staff_id=staff.id)
    context = {
        "staff_result": staff_result,
    }
    return render(request, "staff_template/staff_view_result.html", context)


def view_staff_contract(request):
    view_contract = Staff.objects.get(admin=request.user.id)
    the_contract = Contracts.objects.filter(staff_id=view_contract.id)
    context = {
        "the_contract": the_contract,
    }
    return render(request, "staff_template/contract_view.html", context)


def view_policy(request):
    policy = Policies.objects.all()
    context = {"policy": policy}
    return render(request, "staff_template/policy_view.html", context)


