from django.shortcuts import render,HttpResponse,redirect
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password,check_password
from main.models import auth_table, department_table, student_table, teacher_table
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout



def login(request):
    if 'lid' in request.session:
        del request.session['lid']
    auth_logout(request)
    department  = department_table.objects.all()
    return render(request, 'Login.html',{"departments":department})







def login_function(request):
    username = request.POST['username']
    password = request.POST['password']

    userexist = auth_table.objects.filter(username=username).first()

    if userexist and check_password(password, userexist.password):
        django_user, created = User.objects.get_or_create(username=userexist.username)
        django_user.set_password(userexist.password)  
        django_user.save()

        auth_login(request, django_user)

        request.session['lid'] = userexist.id

        if userexist.role == 'admin':
            return redirect('/admin-dash')
        elif userexist.role == 'teacher':
            return redirect('/teacher-dash')
        elif userexist.role == 'student':
            return redirect('/student-dash')
        else:
            return HttpResponse('Invalid user type')
    else:
        return HttpResponse('<script>alert("Invalid credentials");window.location="/"</script>')


def register(request):
    if 'lid' in request.session:
        del request.session['lid']
    auth_logout(request)

    return render(request, 'Register.html')


def register_logic(request):
        role = request.POST['role']
        username = request.POST['username']
        password = request.POST['password']
        dept_id = request.POST['dept']
        name = request.POST['name']
        age = request.POST['age']
        email = request.POST['email']
        phone = request.POST['phone']
        std_class = request.POST['std_class']
        address = request.POST['address']
        dept = department_table.objects.get(id=dept_id)


        hashed_password = make_password(password)



        if auth_table.objects.filter(username=username).exists():
            return HttpResponse('''<script>alert("username already exist");window.location="/register"</script>''')
        
        
        
        elif role == "student":
            auth = auth_table()
            auth.username=username
            auth.password=hashed_password
            auth.role = 'pending'
            auth.save()


            student = student_table()
            student.LOGIN = auth
            student.name = name
            student.age = age
            student.email = email
            student.phone = phone
            student.DEPT = dept
            student.address = address
            student.std_class = std_class
            student.save()


        else:
            auth = auth_table()
            auth.username=username
            auth.password=hashed_password
            auth.role = role
            auth.save()



            teacher = teacher_table()
            teacher.LOGIN = auth
            teacher.name = name
            teacher.age = age
            teacher.email = email
            teacher.phone = phone
            teacher.DEPT = dept
            teacher.address = address
            teacher.save()


        return HttpResponse('''<script>alert("Registered Successfully!");window.location="/"</script>''')


@login_required(login_url='/')
def admindash(request):
    if 'lid' not in request.session:
        auth_logout(request)
        return redirect('/')

    teachercount = teacher_table.objects.count()
    stdcount = student_table.objects.filter(LOGIN__role='student').count()
    deptcount = department_table.objects.count()


    student_details = student_table.objects.all()

    department_details = department_table.objects.all()

    teachers_details = teacher_table.objects.all()

    details = {
                
        "teachercount": teachercount,
        "stdcount": stdcount,
        "deptcount": deptcount,

        "std_details": student_details,
        "dept_details": department_details,
        "tchr_details": teachers_details,
    }


    return render(request, 'Admin/Dashboard.html',details)


@login_required(login_url='/')
def admin_add_dept(request):
    if 'lid' not in request.session:
        auth_logout(request)
        return redirect('/')
    dept = request.POST['deptname']
    if department_table.objects.filter(department=dept).exists():
        return HttpResponse('''<script>alert("dept alreedy exist");window.location="/admin-dash"</script>''')
    else:
        department =  department_table()
        department.department=dept
        department.save()
    return HttpResponse('''<script>alert("dept added");window.location="/admin-dash"</script>''')


@login_required(login_url='/')
def admin_delete_dept(request,id):
    if 'lid' not in request.session:
        auth_logout(request)
        return redirect('/')
    department = department_table.objects.get(id=id)
    department.delete()
    return HttpResponse('''<script>alert("dept deleted");window.location="/admin-dash"</script>''')


@login_required(login_url='/')
def admin_accpt_std(request,id):
    if 'lid' not in request.session:
        auth_logout(request)
        return redirect('/')
    student = student_table.objects.get(id=id)
    auth = auth_table.objects.get(id=student.LOGIN.id)
    auth.role = 'student'
    auth.save()
    return HttpResponse('''<script>alert("std added");window.location="/admin-dash"</script>''')


@login_required(login_url='/')
def admin_rjct_std(request,id):
    if 'lid' not in request.session:
        auth_logout(request)
        return redirect('/')
    student = student_table.objects.get(id=id)
    auth = auth_table.objects.get(id=student.LOGIN.id)
    auth.role = 'rejected student'
    auth.save()
    return HttpResponse('''<script>alert("rejected student");window.location="/admin-dash"</script>''')



def teacherdash(request):
    if 'lid' not in request.session:
        auth_logout(request)
        return redirect('/')
    teacher = teacher_table.objects.get(LOGIN=request.session['lid'])
    studentcount = student_table.objects.filter(DEPT=teacher.DEPT,LOGIN__role="student").count()
    students = student_table.objects.filter(DEPT=teacher.DEPT)
    departments = department_table.objects.all()
    # print(int(studentcount))

    data = {
        "teacher":teacher,
        "std_count":studentcount,
        "students":students,
        "departments":departments
    }
    

    return render(request,'Teacher/Dashboard.html',data)



def teacher_profile_update(request,id):
    if 'lid' not in request.session:
        auth_logout(request)
        return redirect('/')

    name = request.POST['tname']
    email = request.POST['email']
    phone = request.POST['phone']
    department = request.POST['department']
    address = request.POST['address']


    teacher = teacher_table.objects.get(id=id)
    teacher.name = name
    teacher.email = email
    teacher.phone = phone
    teacher.DEPT = department_table.objects.get(id=department)
    teacher.address = address
    teacher.save()
    return HttpResponse('''<script>alert("profile updated");window.location="/teacher-dash"</script>''')



def studentdash(request):
    if 'lid' not in request.session:
        auth_logout(request)
        return redirect('/')
    student = student_table.objects.get(LOGIN__id=request.session['lid'])
    print(student.name)
    teachers = teacher_table.objects.filter(DEPT=student.DEPT)

    department = department_table.objects.all()

    data = {
        "teachers":teachers,
        "student":student,
        "department":department,
    }





    return render(request,'Student/Dashboard.html',data)

def studentupdateprof(request,id):
    if 'lid' not in request.session:
        auth_logout(request)
        return redirect('/')
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    address = request.POST['address']


    student = student_table.objects.get(id=id)
    student.name = name
    student.email = email
    student.phone = phone
    student.address = address
    student.save()
    return HttpResponse('''<script>alert("profile updated");window.location="/student-dash"</script>''')



def logout(request):
    if 'lid' in request.session:
        del request.session['lid']
    auth_logout(request)
    return redirect('/')