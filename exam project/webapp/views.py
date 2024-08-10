from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .models import profilepic
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        pr=profilepic.objects.all().filter(user=request.user)
        c={"img":pr}
        return render(request,"home.html",context=c)
    else:
        return render(request,"signup.html")

def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method=="POST":
            username=request.POST['username']
            password=request.POST["password"]
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                return redirect('/signin')
        else:
            return render(request,"signup.html")

def signout(request):
    logout(request)
    return redirect('/signin')




def signup(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        confpassword=request.POST['confirmpassword']
        if password==confpassword:
            user=User.objects.create_user(username=username,password=password)
            print(password)
            user.save()

            
            login(request,user)
            return redirect('/')
        else:
            return redirect('/signup')
    else:
        return render(request,"signup.html")
    



from django.shortcuts import redirect, render
from .models import Admen  # Import the Admen model




from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        
        if new_password != confirm_password:
            # Return an error message or redirect if passwords do not match
            return redirect('/')  # Redirecting back to the change password page

        # Check if the current password is correct
        if not request.user.check_password(current_password):
            # Return an error message or redirect if current password is incorrect
            return redirect('/')  # Redirecting back to the change password page
        
        # Set the new password
        request.user.set_password(new_password)
        request.user.save()
        
        # Important: update session to keep the user logged in after changing the password
        update_session_auth_hash(request, request.user)
        
        # Redirect to a success page or elsewhere, indicating password was changed successfully
        return redirect('/')
    else:
        # Render change password form if not a POST request
        return render(request, "/")























from django.http import JsonResponse
from .models import RoomDetails  # Import the RoomDetails model
from django.http import HttpResponse
from django.shortcuts import render
from .models import RoomDetails  # Import the RoomDetails model

def insert_room_details(request):
    if request.method == 'POST':
        try:
            # Retrieve the number of rooms and preset name from the form data
            n = int(request.POST.get('n', 1))
            preset_name = request.POST.get('preset_name')
            
            # Validate the preset name
            if not preset_name:
                return HttpResponse("Preset name cannot be empty", status=400)
            
            # Check if the preset name already exists in the database
            if RoomDetails.objects.filter(user=request.user,preset_name=preset_name).exists():
                return HttpResponse("Preset name already exists in the database", status=400)

            # Loop through the rooms and save the room details
            for i in range(1, n + 1):
                user = request.POST.get('user')
                room_name = request.POST.get(f'room{i}name')
                benches = request.POST.get(f'room{i}benches')
                seats_per_bench = request.POST.get(f'room{i}seats')
                
                # Create and save a new RoomDetails instance
                room_details = RoomDetails(user=user, preset_name=preset_name, room_name=room_name, benches=benches, seats_per_bench=seats_per_bench)
                room_details.save()

            # Return a success message as an HTTP response
            return HttpResponse("Room details saved successfully")

        except Exception as e:
            # Return the error message as an HTTP response with a 500 status code
            return HttpResponse(f"Error: {str(e)}", status=500)

    # If the request method is not POST, return a "Method not allowed" response
    return HttpResponse("Method not allowed", status=405)

from django.shortcuts import render
from django.http import JsonResponse
from .models import Preset

def display_presets(request): 
    
    user = request.user.username
    presets = RoomDetails.objects.filter(user=user).values('preset_name').distinct()
  # Retrieve all records from the RoomDetails table
     
    return render(request, 'presets_template.html', {'user': user, 'presets': presets})






# views.py
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import RoomDetails

@login_required
@csrf_exempt
def delete_preset(request):
    if request.method == 'POST':
        user = request.user
        preset_name = request.POST.get('preset_name')
        if preset_name:
            presets = RoomDetails.objects.filter(user=user, preset_name=preset_name)
            if presets.exists():
                presets.delete()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Preset not found'})
        else:
            return JsonResponse({'success': False, 'message': 'Preset name is required'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})




from django.http import JsonResponse, HttpResponse
from .models import RoomDetails

def fetch_rooms(request):
    # Check if it's a GET request and the X-Requested-With header is set to XMLHttpRequest (commonly set by AJAX requests)
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        preset_name = request.GET.get('preset')
        user = request.GET.get('user')
        rooms = RoomDetails.objects.filter(preset_name=preset_name, user=user)
        room_details = ""
        for room in rooms:
            room_details += f"<p>Room: {room.room_name}, Benches: {room.benches}, Seats per Bench: {room.seats_per_bench}</p>"
        
        return HttpResponse(room_details)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    












from django.shortcuts import render, redirect
import pandas as pd
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .models import Student

@login_required
def upload_file(request):
    query = request.GET.get('query', '')
    students = Student.objects.filter(user=request.user, name__icontains=query) if query else Student.objects.filter(user=request.user)
    context = {
        'students': students,
        'query': query
    }

    if request.method == 'POST' and request.FILES.get('file', None):
        file = request.FILES['file']
        if file.name.endswith('.csv'):
            try:
                with transaction.atomic():
                    df = pd.read_csv(file)
                    
                    for _, row in df.iterrows():
    # Extract student details from each row
                        name = row['Name']
                        phone_number = row['Phone Number']
                        reg_no = row['Registration Number']
                        branch = row['Branch']
                        semester = row['Semester']
    
    # Create a new Student object and save it
                        student = Student.objects.create(
                            user=request.user,
                            name=name,
                            phone_number=phone_number,
                            reg_no=reg_no,
                            branch=branch,
                            semester=semester
                        )
                        print(f"Student {name} with reg no {reg_no} inserted successfully.")
                    context['message'] = 'Students successfully uploaded.'
            except pd.errors.EmptyDataError:
                context['error_message'] = 'Error: Empty CSV file.'
            except pd.errors.ParserError as e:
                context['error_message'] = f'Error: CSV parsing error - {e}'
            except Exception as e:
                context['error_message'] = f'An error occurred while processing the file - {e}'
        else:
            context['error_message'] = 'Error: Invalid file type. Only CSV files are allowed.'

    return render(request, 'student_list_and_add.html', context)







from django.shortcuts import render
from .models import Allocated

from django.shortcuts import render
from .models import Allocated

def search_results(request):
    register_number = request.GET.get('Register_Number')
    print("#######################################################################################")
    print(register_number)
    
    allocated_records = Allocated.objects.filter(reg_no=register_number)
    print(allocated_records)
    
    return render(request, 'signup.html', {'register_number': register_number, 'results': allocated_records})










from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student

@login_required
def student_list_and_add(request):
    query = request.GET.get('query', '')
    branch = request.GET.get('branch', '')
    semester = request.GET.get('semester', '')

    students = Student.objects.filter(user=request.user)

    if query:
        students = students.filter(name__icontains=query)
    if branch:
        students = students.filter(branch=branch)
    if semester:
        students = students.filter(semester=semester)

    if request.method == 'POST' and 'delete' in request.POST:
        ids = request.POST.getlist('ids')
        Student.objects.filter(id__in=ids, user=request.user).delete()
        return redirect('student_list_and_add')

    
    branches = Student.objects.filter(user=request.user).values_list('branch', flat=True).distinct()
    semesters = Student.objects.filter(user=request.user).values_list('semester', flat=True).distinct()

    return render(request, 'student_list_and_add.html', {
        'students': students,
        'query': query,
        'branch': branch,
        'semester': semester,
        'branches': branches,
        'semesters': semesters
    })







@login_required
def student_add(request):
   
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        reg_no = request.POST.get('reg_no')
        branch = request.POST.get('branch')
        semester = request.POST.get('semester')
        
        # Create a new Student instance and save it to the database
        if name and phone_number and reg_no and branch and semester:
            Student.objects.create(
                user=request.user,
                name=name,
                phone_number=phone_number,
                reg_no=reg_no,
                branch=branch,
                semester=semester
            )
            return redirect('student_list_and_add')

    return render(request, 'student_list_and_add.html')

















@login_required
def increment_semester(request):
    students = Student.objects.filter(user=request.user)
    for student in students:
        student.semester += 1
        student.save()
    return JsonResponse({'status': 'success'})

@login_required
def edit_student(request, pk):
    student = Student.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        reg_no = request.POST.get('reg_no')
        branch = request.POST.get('branch')
        semester = request.POST.get('semester')

        # Update the existing Student instance and save it to the database
        if name and phone_number and reg_no and branch and semester:
            student.name = name
            student.phone_number = phone_number
            student.reg_no = reg_no
            student.branch = branch
            student.semester = semester
            student.save()
            return redirect('student_list_and_add')

    return render(request, 'student_list_and_add.html', {
        'student': student,
        'edit': True
    })

@login_required
def delete_student(request, pk):
    student = Student.objects.get(pk=pk, user=request.user)
    student.delete()
    return redirect('student_list_and_add')





















from django.http import JsonResponse
from .models import Student  # Import the Student model or change this as per your model structure
from django.contrib.auth.models import User  # Import the User model if not already imported

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def get_dropdown_data(request):
    if request.method == "GET":
        user_id = request.user.id
        user_students = Student.objects.filter(user_id=user_id)

        if not user_students.exists():
            return JsonResponse({'error': 'No student data found for the user'}, status=404)

        # Prepare data structure: branches to semesters mapping
        branch_to_semesters = {}
        for student in user_students:
            branch = student.branch
            semester = student.semester
            if branch not in branch_to_semesters:
                branch_to_semesters[branch] = set()
            branch_to_semesters[branch].add(semester)

        # Convert sets to lists for JSON serialization
        for branch in branch_to_semesters:
            branch_to_semesters[branch] = list(branch_to_semesters[branch])

        # Return the data as JSON response
        return JsonResponse(branch_to_semesters)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
















# views.py


import random
from django.http import JsonResponse
from django.http import JsonResponse
import random


from django.http import JsonResponse

from django.http import HttpResponse


import random

import random

def greedy_coloring(room_names, room_benches, seats_per_bench, subjects_info, sub,edate,user_id):
    # Input validation
    if len(room_names) != len(room_benches) or len(room_names) != len(seats_per_bench):
        raise ValueError("Number of room names, room benches, and seats per bench should match.")

    students = []  # List to store student information

    # Populate students list with student information based on subjects_info
    for subject, num_students in subjects_info.items():
        for i in range(1, num_students + 1):
            # Accessing the name and subject from the subject_data dictionary
            name = sub[subject][f'{subject}{i}']['name']
            reg_no = sub[subject][f'{subject}{i}']['reg_no']
            # Extract the last 3 characters of the registration number as digits
            reg_no_digit = int(reg_no[-3:])
            # Appending the student object to the students list
            students.append({'name': name, 'reg_no': reg_no, 'subject': subject, 'reg_no_digit': reg_no_digit})

    # Sort the students list in registration number order
    students.sort(key=lambda x: x['reg_no_digit'])

    # Ensure that the first student in the list always has the lowest registration number
    if students[0]['reg_no_digit'] != int(students[0]['reg_no'][-3:]):
        students.insert(0, students.pop(students.index(students[0])))

    # Initialize a dictionary to store the colors (subjects) assigned to each student
    student_colors = {}

    # Initialize a dictionary to store the seats allocated for each bench in each room
    bench_allocation = {room_name: {i: [] for i in range(1, room_benches[room_names.index(room_name)] + 1)} for
                        room_name in room_names}

    # Initialize a temporary dictionary to store allocation details
    allocation_details1 = {}

    # Greedy coloring algorithm
    for student in sorted(students, key=lambda x: x['reg_no_digit']):
        allocated_bench = False

        # Iterate over the rooms and benches in ascending order
        for room_name in room_names:
            for bench_num in range(1, room_benches[room_names.index(room_name)] + 1):
                subject_count = sum(1 for s in bench_allocation[room_name][bench_num] if
                                    s['subject'] == student['subject'])
                if subject_count < 2 and len(bench_allocation[room_name][bench_num]) < seats_per_bench[
                    room_names.index(room_name)]:
                    # Check if there is a student with a different subject to insert the current student
                    if bench_allocation[room_name][bench_num]:
                        prev_student_subject = bench_allocation[room_name][bench_num][-1]['subject']
                        if prev_student_subject != student['subject']:
                            seat_num = len(bench_allocation[room_name][bench_num]) + 1
                            bench_allocation[room_name][bench_num].append(student)
                            allocated_bench = True
                            print(f"Allocated {student['name']} to bench {bench_num}, seat {seat_num} in room {room_name}")
                            # Store allocation details
                            allocation_details1[student['name']] = {
                                'reg_no': student['reg_no'],
                                'room': room_name,
                                'bench': bench_num,
                                'seat': seat_num
                            }
                            break
                    else:
                        seat_num = 1
                        bench_allocation[room_name][bench_num].append(student)
                        allocated_bench = True
                        print(f"Allocated {student['name']} to bench {bench_num}, seat {seat_num} in room {room_name}")
                        # Store allocation details
                        allocation_details1[student['name']] = {
                            'reg_no': student['reg_no'],
                            'room': room_name,
                            'bench': bench_num,
                            'seat': seat_num
                        }
                        break
            if allocated_bench:
                break

        if not allocated_bench:
            print(f"Failed to allocate {student['name']}")
            raise ValueError("Not enough seats available for the subjects.")

        # Update the colors assigned to the student
        student_colors[student['name']] = student['subject']

    # Print allocation details
    
    
        
    stored_data = []
    print("///////////////////////////////Allocation Details:")

    # Iterate over allocation_details
    for student_name, details in allocation_details1.items():
        # Get the student object from the students list using the name
        student = next(s for s in students if s['name'] == student_name)

        # Create a new dictionary for each student
        student_data = {
            'name': student_name,
            'reg': details['reg_no'],
            'room': details['room'],
            'bench': details['bench'],
            'seat': details['seat'],
            'subject': student['subject'], # Add the subject field
            'user_id': user_id,
            'date': str(edate)
        }
        print(
            f"Name: {student_name}, Reg No: {details['reg_no']}, Room: {details['room']}, Bench: {details['bench']}, Seat: {details['seat']}")
        # Append the student data dictionary to the list
        stored_data.append(student_data)

    allocation_details = stored_data
    print("-------------------------------------------------------")
    print(allocation_details)

    return bench_allocation, student_colors, allocation_details
























from django.shortcuts import render

def seat_allocation(request):
    if request.method == 'POST':
        edate = request.POST.get('birthdate')
        user_id = request.user.id
        form_data = request.POST
        
        try:
            total_rooms = int(form_data.get('total-rooms', 0))
            num_subjects = int(form_data.get('num-subjects', 0))
            user_id = request.user.id
            room_names = []
            room_benches = []
            seats_per_bench_list = []
            subjects_info = {}
            sub = {}
            
            for i in range(total_rooms):
                room_name = form_data.get(f'room-name-{i}', f"Room{i+1}")
                benches = int(form_data.get(f'room-benches-{i}', 0))
                seats_per_bench = int(form_data.get(f'room-seats-{i}', 0))
                
                room_names.append(room_name)
                room_benches.append(benches)
                seats_per_bench_list.append(seats_per_bench)
            
            for i in range(num_subjects):
                sub_name = form_data.get(f'subject-name-{i+1}', f'Subject{i+1}')
                branch = form_data.get(f'branch-{i+1}', 'Unknown')
                semester = int(form_data.get(f'semester-{i+1}', '1'))  # Convert to int
                
                student_count = get_student_count_internal(user_id, branch, semester)
                subjects_info[sub_name] = student_count
                sub[sub_name] = getsub(user_id, branch, semester, sub_name)
           
            print('subject:', sub)
            print('Form Data:')
            print('total_rooms:', total_rooms)
            print('room_names:', room_names)
            print('room_benches:', room_benches)
            print('seats_per_bench_list:', seats_per_bench_list)
            print('subjects_info:', subjects_info)
           
            # Call the greedy_coloring function for seat allocation
            allocation_result, student_colors, allocation_details = greedy_coloring(room_names, room_benches, seats_per_bench_list, subjects_info, sub,edate,user_id)
            context = {
                'total_rooms': total_rooms,
                'allocation_result': allocation_result,
                'student_colors': student_colors,
                'data_to_send': allocation_details
            }
            print("--------------------------------------allocation result-----------------------------------")
            print(allocation_details)
            
            # Check if the button responsible for insertion is clicked
            print(context['data_to_send'])
            return render(request, 'seat_allocation_result.html', context)
        
        except ValueError as e:
            return render(request, 'error.html', {'error': str(e)})
    
    # Handle non-POST requests or initial form display
    return render(request, 'presets_template.html')
















from django.http import JsonResponse
import json

def collect_data(request):
    if request.method == 'POST':
        received_data = json.loads(request.body)
        print("----------------------------received_data---------------------")
        print(received_data) 
         # Do something with the received data
        result = insert_data_into_db(received_data)
        return JsonResponse({'message': 'Data received successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)







from django.http import JsonResponse
from webapp.models import Student

def get_phone_number(reg_no, user_id):
    try:
        # Query the Student model based on the registration number and user ID
        student = Student.objects.get(reg_no=reg_no, user_id=user_id)
        
        # Retrieve the phone number of the student
        phone_number = student.phone_number
        
        # Return the phone number
        return phone_number
    except Student.DoesNotExist:
        # If no student with the provided registration number and user ID is found, return an error response
        return JsonResponse({'message': 'Student not found'}, status=404)









# Insert into database table
# Insert into database table
# Insert into database table
import pywhatkit
from datetime import datetime
from datetime import datetime, timedelta
from django.http import JsonResponse
from webapp.models import Allocated

def insert_data_into_db(data_list):
    print("ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
    for data in data_list:
        # Check if a record with the same combination of registration number, subject, and date exists
        existing_record = Allocated.objects.filter(
            reg_no=data['reg'],
            subject=data['subject'],
            date=data['date']
        ).first()

        # If no record exists, create a new one
        if not existing_record:
            student = Allocated.objects.create(
                student_name=data['name'],
                reg_no=data['reg'],
                room=data['room'],
                bench=data['bench'],
                seat=data['seat'],
                user=data['user_id'],
                subject=data['subject'],
                date=data['date']
            )
            student.save()
            phno=get_phone_number(data['reg'], data['user_id'])
            print(student)
            print(phno)
            message = f"Hi dear {data['name']} \n  You are sitting in Room {data['room']}, Bench {data['bench']} in seat {data['seat']} for {data['subject']} exam on {data['date']} \n best wishes"
            
            current_time = datetime.now()
            current_hour = current_time.hour
            current_minute = current_time.minute

            current_minute += 1

# Adjust hour if minute reaches 60
            if current_minute == 60:
                current_hour += 2
                current_minute = 0

            print("Current time:", current_hour, "hours", current_minute, "minutes")
            pywhatkit.sendwhatmsg(phno, message, current_hour, current_minute, 30,True,3)
            print("----------------------------ok---------------------")
        else:
            print("----------------------------duplicate---------------------")
            # If a record already exists, return a JSON response with the alert message
            return JsonResponse({'message': 'Some students have already been allocated this subject on this date.'}, status=400)

    # If all records are successfully inserted, return a success message
    return JsonResponse({'message': 'Data inserted successfully'}, status=200)










from django.shortcuts import render
from .models import Student
def get_student_count_internal(user_id,branch, semester):
    # Assuming you have a Student model with fields 'branch' and 'semester'
    if not branch or not semester:
        return None  # or raise an exception, depending on your requirement

    student_count = Student.objects.filter(user_id=user_id,branch=branch, semester=semester).count()

    return student_count
    
from django.shortcuts import render
from .models import Student

def getsub(user_id, branch, semester, sub_names):
    # Assuming you have a Student model with fields 'branch' and 'semester'
    if not branch or not semester:
        return None  # or raise an exception, depending on your requirement

    subs = Student.objects.filter(user_id=user_id, branch=branch, semester=semester).values('name', 'reg_no')

    # Initialize a dictionary to store the retrieved data
    data = {}

    # Initialize a counter variable to generate keys like 'sub_name1', 'sub_name2', etc.
    i = 1

    # Save the retrieved data with keys like 'sub_name1', 'sub_name2', etc.
    for sub in subs:
        data[f"{sub_names}{i}"] = sub
        i += 1

    return data


