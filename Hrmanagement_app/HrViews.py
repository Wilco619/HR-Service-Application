from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.db import IntegrityError

import json

from Hrmanagement_app.models import CustomUser, Manager, Department, Position, Staff, ContractYearModel, FeedBackStaff, FeedBackManager, LeaveReportStaff, LeaveReportManager, Attendance, AttendanceReport
from .forms import AddStaffForm, EditStaffForm
    

def admin_home(request):
    all_staff_count = Staff.objects.all().count()
    position_count = Position.objects.all().count()
    department_count = Department.objects.all().count()
    manager_count = Manager.objects.all().count()

    # Total Position and staffs in Each Department
    department_all = Department.objects.all()
    department_name_list = []
    position_count_list = []
    staff_count_list_in_department = []

    for department in department_all:
        positions = Position.objects.filter(department_id=department.id).count()
        staffs = Staff.objects.filter(department_id=department.id).count()
        department_name_list.append(department.department_name)
        position_count_list.append(positions)
        staff_count_list_in_department.append(staffs)
    
    position_all = Position.objects.all()
    position_list = []
    staff_count_list_in_position = []
    for position in position_all:
        department = Department.objects.get(id=position.department_id.id)
        staff_count = Staff.objects.filter(department_id=department.id).count()
        position_list.append(position.position_name)
        staff_count_list_in_position.append(staff_count)
    
    # For Saffs
    manager_attendance_present_list=[]
    manager_attendance_leave_list=[]
    manager_name_list=[]

    managers = Manager.objects.all()
    for manager in managers:
        position_ids = Position.objects.filter(manager_id=manager.admin.id)
        attendance = Attendance.objects.filter(position_id__in=position_ids).count()
        leaves = LeaveReportManager.objects.filter(manager_id=manager.id, leave_status=1).count()
        manager_attendance_present_list.append(attendance)
        manager_attendance_leave_list.append(leaves)
        manager_name_list.append(manager.admin.first_name)

    # For Staff
    staff_attendance_present_list=[]
    staff_attendance_leave_list=[]
    staff_name_list=[]

    staffs = Staff.objects.all()
    for staff in staffs:
        attendance = AttendanceReport.objects.filter(staff_id=staff.id, status=True).count()
        absent = AttendanceReport.objects.filter(staff_id=staff.id, status=False).count()
        leaves = LeaveReportStaff.objects.filter(staff_id=staff.id, leave_status=1).count()
        staff_attendance_present_list.append(attendance)
        staff_attendance_leave_list.append(leaves+absent)
        staff_name_list.append(staff.admin.first_name)


    context={
        "all_staff_count": all_staff_count,
        "position_count": position_count,
        "department_count": department_count,
        "manager_count": manager_count,
        "department_name_list": department_name_list,
        "position_count_list": position_count_list,
        "staff_count_list_in_department": staff_count_list_in_department,
        "position_list": position_list,
        "staff_count_list_in_position": staff_count_list_in_position,
        "manager_attendance_present_list": manager_attendance_present_list,
        "manager_attendance_leave_list": manager_attendance_leave_list,
        "manager_name_list": manager_name_list,
        "staff_attendance_present_list": staff_attendance_present_list,
        "staff_attendance_leave_list": staff_attendance_leave_list,
        "staff_name_list": staff_name_list,
    }
    return render(request, "hod_template/home_content.html", context)


def add_manager(request):
    return render(request, "hod_template/add_manager_template.html")

def add_manager_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method ")
        return redirect('add_manager')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            # Creating a new user with the CustomUser model
            user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)

            # Adding address to the Manager model associated with the user
            user.manager.address = address
            user.manager.save()

            messages.success(request, "Manager Added Successfully!")
            return redirect('add_manager')
        except IntegrityError as e:
            messages.error(request, f"Failed to Add Manager. {e}")
            return redirect('add_manager')

def manage_manager(request):
    managers = Manager.objects.all()
    context = {
        "managers": managers
    }
    return render(request, "hod_template/manage_manager_template.html", context)

def edit_manager(request, manager_id):
    manager = Manager.objects.get(admin=manager_id)

    context = {
        "manager": manager,
        "id": manager_id
    }
    return render(request, "hod_template/edit_manager_template.html", context)

def edit_manager_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        manager_id = request.POST.get('manager_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')

        try:
            # Updating the CustomUser model
            user = CustomUser.objects.get(id=manager_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()

            # Updating the Manager model
            manager_model = Manager.objects.get(admin=manager_id)
            manager_model.address = address
            manager_model.save()

            messages.success(request, "Manager Updated Successfully.")
            return redirect(reverse('edit_manager', args=[manager_id]))

        except CustomUser.DoesNotExist:
            messages.error(request, "Manager not found.")
            return redirect('manage_manager')
        except IntegrityError as e:
            messages.error(request, f"Failed to Update Manager. {e}")
            return redirect(reverse('edit_manager', args=[manager_id]))

def delete_manager(request, manager_id):
    try:
        manager = Manager.objects.get(admin=manager_id)
        manager.delete()
        messages.success(request, "Manager Deleted Successfully.")
    except Manager.DoesNotExist:
        messages.error(request, "Manager not found.")
    except Exception as e:
        messages.error(request, f"Failed to Delete Manager. {e}")

    return redirect('manage_manager')



def add_department(request):
    return render(request, "hod_template/add_department_template.html")


def add_department_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_department')
    else:
        department = request.POST.get('department')
        try:
            department_model = Department(department_name=department)
            department_model.save()
            messages.success(request, "Department Added Successfully!")
            return redirect('add_department')
        except:
            messages.error(request, "Failed to Add Department!")
            return redirect('add_department')


def manage_department(request):
    departments = Department.objects.all()
    context = {
        "departments": departments
    }
    return render(request, 'hod_template/manage_department_template.html', context)


def edit_department(request, department_id):
    department = Department.objects.get(id=department_id)
    context = {
        "department": department,
        "id": department_id
    }
    return render(request, 'hod_template/edit_department_template.html', context)


def edit_department_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        department_id = request.POST.get('department_id')
        department_name = request.POST.get('department')

        try:
            department = Department.objects.get(id=department_id)
            department.department_name = department_name
            department.save()

            messages.success(request, "Department Updated Successfully.")
            return redirect('/edit_department/'+department_id)

        except:
            messages.error(request, "Failed to Update Department.")
            return redirect('/edit_department/'+department_id)


def delete_department(request, department_id):
    department = Department.objects.get(id=department_id)
    try:
        department.delete()
        messages.success(request, "Department Deleted Successfully.")
        return redirect('manage_department')
    except:
        messages.error(request, "Failed to Delete Department.")
        return redirect('manage_department')


def manage_contract(request):
    contract_years = ContractYearModel.objects.all()
    context = {
        "contract_years": contract_years
    }
    return render(request, "hod_template/manage_contract_template.html", context)


def add_contract(request):
    return render(request, "hod_template/add_contract_template.html")


def add_contract_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_department')
    else:
        contract_start_year = request.POST.get('contract_start_year')
        contract_end_year = request.POST.get('contract_end_year')

        try:
            contractyear = ContractYearModel(contract_start_year=contract_start_year, contract_end_year=contract_end_year)
            contractyear.save()
            messages.success(request, "Contract Year added Successfully!")
            return redirect("add_contract")
        except:
            messages.error(request, "Failed to Add Contract Year")
            return redirect("add_contract")


def edit_contract(request, contract_id):
    contract_year = ContractYearModel.objects.get(id=contract_id)
    context = {
        "contract_year": contract_year
    }
    return render(request, "hod_template/edit_contract_template.html", context)


def edit_contract_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_contract')
    else:
        contract_id = request.POST.get('contract_id')
        contract_start_year = request.POST.get('contract_start_year')
        contract_end_year = request.POST.get('contract_end_year')

        try:
            contract_year = ContractYearModel.objects.get(id=contract_id)
            contract_year.contract_start_year = contract_start_year
            contract_year.contract_end_year = contract_end_year
            contract_year.save()

            messages.success(request, "Contract Year Updated Successfully.")
            return redirect('/edit_contract/'+contract_id)
        except:
            messages.error(request, "Failed to Update Contract Year.")
            return redirect('/edit_contract/'+contract_id)


def delete_contract(request, contract_id):
    contract = ContractYearModel.objects.get(id=contract_id)
    try:
        contract.delete()
        messages.success(request, "Contract Deleted Successfully.")
        return redirect('manage_contract')
    except:
        messages.error(request, "Failed to Delete Contract.")
        return redirect('manage_contract')

def add_staff(request):
    form = AddStaffForm()
    context = {"form": form}
    return render(request, 'hod_template/add_staff_template.html', context)

def add_staff_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_staff')
    else:
        form = AddStaffForm(request.POST, request.FILES)

        if form.is_valid():
            # Extract cleaned data from the form
            # ...
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            contract_year_id = form.cleaned_data['contract_year_id']
            department_id = form.cleaned_data['department_id']
            gender = form.cleaned_data['gender']
            phone = form.cleaned_data['phone']
            i_d = form.cleaned_data['i_d']

            # Getting Profile Pic first
            if 'profile_pic' in request.FILES:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                # Create user and associate with staff model
                user = CustomUser.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    user_type=3
                )
                user.staff.address = address
                user.staff.department_id = Department.objects.get(id=department_id)
                user.staff.contract_year_id = ContractYearModel.objects.get(id=contract_year_id)
                user.staff.gender = gender
                user.staff.phone = phone
                user.staff.i_d = i_d
                user.staff.profile_pic = profile_pic_url
                user.save()
                messages.success(request, "Manager Added Successfully!")
                return redirect('add_staff')
            except Exception as e:
                messages.error(request, f"Failed to Add Manager. {str(e)}")
                return redirect('add_staff')
        else:
            messages.error(request, "Form is not valid. Please check the form.")
            return redirect('add_staff')


def manage_staff(request):
    staffs = Staff.objects.all()
    context = {
        "staffs": staffs
    }
    return render(request, 'hod_template/manage_staff_template.html', context)


def edit_staff(request, staff_id):
    # Adding Staff ID into Contract Variable
    request.session['staff_id'] = staff_id

    staff = Staff.objects.get(admin=staff_id)
    form = EditStaffForm()
    # Filling the form with Data from Database
    form.fields['email'].initial = staff.admin.email
    form.fields['username'].initial = staff.admin.username
    form.fields['first_name'].initial = staff.admin.first_name
    form.fields['last_name'].initial = staff.admin.last_name
    form.fields['address'].initial = staff.address
    form.fields['department_id'].initial = staff.department_id.id
    form.fields['gender'].initial = staff.gender
    form.fields['phone'].initial = staff.phone
    form.fields['i_d'].initial = staff.i_d
    form.fields['contract_year_id'].initial = staff.contract_year_id.id

    context = {
        "id": staff_id,
        "username": staff.admin.username,
        "form": form
    }
    return render(request, "hod_template/edit_staff_template.html", context)


def edit_staff_save(request):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        staff_id = request.session.get('staff_id')
        if staff_id == None:
            return redirect('/manage_staff')

        form = EditStaffForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            address = form.cleaned_data['address']
            department_id = form.cleaned_data['department_id']
            gender = form.cleaned_data['gender']
            phone = form.cleaned_data['phone']
            i_d = form.cleaned_data['i_d']
            contract_year_id = form.cleaned_data['contract_year_id']

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
            if len(request.FILES) != 0:
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None

            try:
                # First Update into Custom User Model
                user = CustomUser.objects.get(id=staff_id)
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.username = username
                user.save()

                # Then Update Staff Table
                staff_model = Staff.objects.get(admin=staff_id)
                staff_model.address = address

                department = Department.objects.get(id=department_id)
                staff_model.department_id = department

                contract_year_obj = ContractYearModel.objects.get(id=contract_year_id)
                staff_model.contract_year_id = contract_year_obj

                staff_model.gender = gender
                staff_model.phone = phone
                staff_model.i_d = i_d
                if profile_pic_url != None:
                    staff_model.profile_pic = profile_pic_url
                staff_model.save()
                # Delete staff_id SESSION after the data is updated
                del request.contract['staff_id']

                messages.success(request, "Manager Updated Successfully!")
                return redirect('/edit_staff/'+staff_id)
            except:
                messages.success(request, "Failed to Update Manager.")
                return redirect('/edit_staff/'+staff_id)
        else:
            return redirect('/edit_staff/'+staff_id)


def delete_staff(request, staff_id):
    staff = Staff.objects.get(admin=staff_id)
    try:
        staff.delete()
        messages.success(request, "Manager Deleted Successfully.")
        return redirect('manage_staff')
    except:
        messages.error(request, "Failed to Delete Manager.")
        return redirect('manage_staff')


def add_position(request):
    departments = Department.objects.all()
    managers = CustomUser.objects.filter(user_type='2')
    context = {
        "departments": departments,
        "managers": managers
    }
    return render(request, 'hod_template/add_position_template.html', context)



def add_position_save(request):
    if request.method != "POST":
        messages.error(request, "Method Not Allowed!")
        return redirect('add_position')
    else:
        position_name = request.POST.get('position')

        department_id = request.POST.get('department')
        department = Department.objects.get(id=department_id)
        
        manager_id = request.POST.get('manager')
        manager = CustomUser.objects.get(id=manager_id)

        try:
            position = Position(position_name=position_name, department_id=department, manager_id=manager)
            position.save()
            messages.success(request, "Position Added Successfully!")
            return redirect('add_position')
        except:
            messages.error(request, "Failed to Add Position!")
            return redirect('add_position')


def manage_position(request):
    positions = Position.objects.all()
    context = {
        "positions": positions
    }
    return render(request, 'hod_template/manage_position_template.html', context)


def edit_position(request, position_id):
    position = Position.objects.get(id=position_id)
    departments = Department.objects.all()
    managers = CustomUser.objects.filter(user_type='2')
    context = {
        "position": position,
        "departments": departments,
        "managers": managers,
        "id": position_id
    }
    return render(request, 'hod_template/edit_position_template.html', context)


def edit_position_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method.")
    else:
        position_id = request.POST.get('position_id')
        position_name = request.POST.get('position')
        department_id = request.POST.get('department')
        manager_id = request.POST.get('manager')

        try:
            position = Position.objects.get(id=position_id)
            position.position_name = position_name

            department = Department.objects.get(id=department_id)
            position.department_id = department

            manager = CustomUser.objects.get(id=manager_id)
            position.manager_id = manager
            
            position.save()

            messages.success(request, "Position Updated Successfully.")
            # return redirect('/edit_position/'+position_id)
            return HttpResponseRedirect(reverse("edit_position", kwargs={"position_id":position_id}))

        except:
            messages.error(request, "Failed to Update Position.")
            return HttpResponseRedirect(reverse("edit_position", kwargs={"position_id":position_id}))
            # return redirect('/edit_position/'+position_id)



def delete_position(request, position_id):
    position = Position.objects.get(id=position_id)
    try:
        position.delete()
        messages.success(request, "Position Deleted Successfully.")
        return redirect('manage_position')
    except:
        messages.error(request, "Failed to Delete Position.")
        return redirect('manage_position')


@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj = CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)


@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)



def staff_feedback_message(request):
    feedbacks = FeedBackStaff.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/staff_feedback_template.html', context)


@csrf_exempt
def staff_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackStaff.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def manager_feedback_message(request):
    feedbacks = FeedBackManager.objects.all()
    context = {
        "feedbacks": feedbacks
    }
    return render(request, 'hod_template/manager_feedback_template.html', context)


@csrf_exempt
def manager_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')

    try:
        feedback = FeedBackManager.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")


def staff_leave_view(request):
    leaves = LeaveReportStaff.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/staff_leave_view.html', context)

def staff_leave_approve(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('staff_leave_view')


def staff_leave_reject(request, leave_id):
    leave = LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('staff_leave_view')


def manager_leave_view(request):
    leaves = LeaveReportManager.objects.all()
    context = {
        "leaves": leaves
    }
    return render(request, 'hod_template/manager_leave_view.html', context)


def manager_leave_approve(request, leave_id):
    leave = LeaveReportManager.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return redirect('manager_leave_view')


def manager_leave_reject(request, leave_id):
    leave = LeaveReportManager.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return redirect('manager_leave_view')


def admin_view_attendance(request):
    positions = Position.objects.all()
    contract_years = ContractYearModel.objects.all()
    context = {
        "positions": positions,
        "contract_years": contract_years
    }
    return render(request, "hod_template/admin_view_attendance.html", context)


@csrf_exempt
def admin_get_attendance_dates(request):
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
        data_small={"id":attendance_single.id, "attendance_date":str(attendance_single.attendance_date), "contract_year_id":attendance_single.contract_year_id.id}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def admin_get_attendance_staff(request):
    # Getting Values from Ajax POST 'Fetch Staff'
    attendance_date = request.POST.get('attendance_date')
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    # Only Passing Staff Id and Staff Name Only
    list_data = []

    for staff in attendance_data:
        data_small={"id":staff.staff_id.admin.id, "name":staff.staff_id.admin.first_name+" "+staff.staff_id.admin.last_name, "status":staff.status}
        list_data.append(data_small)

    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)

    context={
        "user": user
    }
    return render(request, 'hod_template/admin_profile.html', context)


def admin_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('admin_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('admin_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('admin_profile')
    


def manager_profile(request):
    pass


def staff_profile(requtest):
    pass



