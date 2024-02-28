from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from Hrmanagement_app.models import CustomUser, Staff, Department, Position, Manager, ContractYearModel, Attendance, \
    AttendanceReport, LeaveReportManager, FeedBackManager, StaffPoint


def manager_home(request):
    # Fetching All Staff under Manager

    positions = Position.objects.filter(manager_id=request.user.id)
    department_id_list = []
    for position in positions:
        department = Department.objects.get(id=position.department_id.id)
        department_id_list.append(department.id)

    final_department = []
    # Removing Duplicate Department Id
    for department_id in department_id_list:
        if department_id not in final_department:
            final_department.append(department_id)

    staffs_count = Staff.objects.filter(department_id__in=final_department).count()
    position_count = positions.count()

    # Fetch All Attendance Count
    attendance_count = Attendance.objects.filter(position_id__in=positions).count()
    # Fetch All Approve Leave
    manager = Manager.objects.get(admin=request.user.id)
    leave_count = LeaveReportManager.objects.filter(manager_id=manager.id, leave_status=1).count()

    # Fetch Attendance Data by Position
    position_list = []
    attendance_list = []
    for position in positions:
        attendance_count1 = Attendance.objects.filter(position_id=position.id).count()
        position_list.append(position.position_name)
        attendance_list.append(attendance_count1)

    staffs_attendance = Staff.objects.filter(department_id__in=final_department)
    staff_list = []
    staff_list_attendance_present = []
    staff_list_attendance_absent = []
    for staff in staffs_attendance:
        attendance_present_count = AttendanceReport.objects.filter(status=True, staff_id=staff.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(status=False, staff_id=staff.id).count()
        staff_list.append(staff.admin.first_name + " " + staff.admin.last_name)
        staff_list_attendance_present.append(attendance_present_count)
        staff_list_attendance_absent.append(attendance_absent_count)

    context = {
        "staffs_count": staffs_count,
        "attendance_count": attendance_count,
        "leave_count": leave_count,
        "position_count": position_count,
        "position_list": position_list,
        "attendance_list": attendance_list,
        "staff_list": staff_list,
        "attendance_present_list": staff_list_attendance_present,
        "attendance_absent_list": staff_list_attendance_absent
    }
    return render(request, "manager_template/manager_home_template.html", context)


def manager_take_attendance(request):
    positions = Position.objects.filter(manager_id=request.user.id)
    contract_years = ContractYearModel.objects.all()
    context = {
        "positions": positions,
        "contract_years": contract_years
    }
    return render(request, "manager_template/take_attendance_template.html", context)


def manager_apply_leave(request):
    manager_obj = Manager.objects.get(admin=request.user.id)
    leave_data = LeaveReportManager.objects.filter(manager_id=manager_obj)
    context = {
        "leave_data": leave_data
    }
    return render(request, "manager_template/manager_apply_leave_template.html", context)


def manager_apply_leave_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('manager_apply_leave')
    else:
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')

        manager_obj = Manager.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportManager(manager_id=manager_obj, leave_date=leave_date,
                                              leave_message=leave_message, leave_status=0)
            leave_report.save()
            messages.success(request, "Applied for Leave.")
            return redirect('manager_apply_leave')
        except:
            messages.error(request, "Failed to Apply Leave")
            return redirect('manager_apply_leave')


def manager_feedback(request):
    manager_obj = Manager.objects.get(admin=request.user.id)
    feedback_data = FeedBackManager.objects.filter(manager_id=manager_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, "manager_template/manager_feedback_template.html", context)


def manager_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('manager_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        manager_obj = Manager.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackManager(manager_id=manager_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('manager_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('manager_feedback')


# WE don't need csrf_token when using Ajax
@csrf_exempt
def get_staffs(request):
    # Getting Values from Ajax POST 'Fetch Staff'
    position_id = request.POST.get("position")
    contract_year = request.POST.get("contract_year")

    # Staff enroll to Department, Department has Position
    # Getting all data from position model based on position_id
    position_model = Position.objects.get(id=position_id)

    contract_model = ContractYearModel.objects.get(id=contract_year)

    staffs = Staff.objects.filter(department_id=position_model.department_id, contract_year_id=contract_model)

    # Only Passing Staff Id and Staff Name Only
    list_data = []

    for staff in staffs:
        data_small = {"id": staff.admin.id, "name": staff.admin.first_name + " " + staff.admin.last_name}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def save_attendance_data(request):
    # Get Values from Staf Take Attendance form via AJAX (JavaScript)
    # Use getlist to access HTML Array/List Input Data
    staff_ids = request.POST.get("staff_ids")
    position_id = request.POST.get("position_id")
    attendance_date = request.POST.get("attendance_date")
    contract_year_id = request.POST.get("contract_year_id")

    position_model = Position.objects.get(id=position_id)
    contract_year_model = ContractYearModel.objects.get(id=contract_year_id)

    json_staff = json.loads(staff_ids)
    # print(dict_staff[0]['id'])

    # print(staff_ids)
    try:
        # First Attendance Data is Saved on Attendance Model
        attendance = Attendance(position_id=position_model, attendance_date=attendance_date,
                                contract_year_id=contract_year_model)
        attendance.save()

        for stud in json_staff:
            # Attendance of Individual Staff saved on AttendanceReport Model
            staff = Staff.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(staff_id=staff, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")


def manager_update_attendance(request):
    positions = Position.objects.filter(manager_id=request.user.id)
    contract_years = ContractYearModel.objects.all()
    context = {
        "positions": positions,
        "contract_years": contract_years
    }
    return render(request, "manager_template/update_attendance_template.html", context)


@csrf_exempt
def get_attendance_dates(request):
    # Getting Values from Ajax POST 'Fetch Staff'
    position_id = request.POST.get("position")
    contract_year = request.POST.get("contract_year_id")

    # Staff enroll to Department, Department has Position
    # Getting all data from position model based on position_id
    position_model = Position.objects.get(id=position_id)

    contract_model = ContractYearModel.objects.get(id=contract_year)

    # staffs = Staff.objects.filter(department_id=position_model.department_id, contract_year_id=contract_model)
    attendance = Attendance.objects.filter(position_id=position_model, contract_year_id=contract_model)

    # Only Passing Staff Id and Staff Name Only
    list_data = []

    for attendance_single in attendance:
        data_small = {"id": attendance_single.id, "attendance_date": str(attendance_single.attendance_date),
                      "contract_year_id": attendance_single.contract_year_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def get_attendance_staff(request):
    # Getting Values from Ajax POST 'Fetch Staff'
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Staff Id and Staff Name Only
    list_data = []

    for staff in attendance_data:
        data_small = {"id": staff.staff_id.admin.id,
                      "name": staff.staff_id.admin.first_name + " " + staff.staff_id.admin.last_name,
                      "status": staff.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def update_attendance_data(request):
    staff_ids = request.POST.get("staff_ids")

    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    json_staff = json.loads(staff_ids)

    try:

        for stud in json_staff:
            # Attendance of Individual Staff saved on AttendanceReport Model
            staff = Staff.objects.get(admin=stud['id'])

            attendance_report = AttendanceReport.objects.get(staff_id=staff, attendance_id=attendance)
            attendance_report.status = stud['status']

            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("Error")


def manager_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    manager = Manager.objects.get(admin=user)

    context = {
        "user": user,
        "manager": manager
    }
    return render(request, 'manager_template/manager_profile.html', context)


def manager_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manager_profile')
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

            manager = Manager.objects.get(admin=customuser.id)
            manager.address = address
            manager.save()

            messages.success(request, "Profile Updated Successfully")
            return redirect('manager_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('manager_profile')


def manager_add_result(request):
    positions = Position.objects.filter(manager_id=request.user.id)
    contract_years = ContractYearModel.objects.all()
    context = {
        "positions": positions,
        "contract_years": contract_years,
    }
    return render(request, "manager_template/add_result_template.html", context)


def manager_add_result_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('manager_add_result')
    else:
        staff_admin_id = request.POST.get('staff_list')
        bonus = request.POST.get('bonus')
        incentive = request.POST.get('incentive')
        position_id = request.POST.get('position')

        try:
            staff_obj = Staff.objects.get(admin=staff_admin_id)
            position_obj = Position.objects.get(id=position_id)

            # Check if Staff Result Already Exists or not
            check_exist = StaffPoint.objects.filter(position_id=position_obj, staff_id=staff_obj).exists()
            if check_exist:
                result = StaffPoint.objects.get(position_id=position_obj, staff_id=staff_obj)
                result.position_bonus_point = bonus
                result.position_incentive_point = incentive
                result.save()
                messages.success(request, "Points Updated Successfully!")
            else:
                result = StaffPoint(staff_id=staff_obj, position_id=position_obj, position_incentive_point=incentive,
                                    position_bonus_point=bonus)
                result.save()
                messages.success(request, "Points Added Successfully!")
        except ObjectDoesNotExist:
            messages.error(request, "Staff or Position does not exist.")
        except Exception as e:
            messages.error(request, f"Failed to Add Bonus/Incentive: {str(e)}")

        return redirect('manager_add_result')