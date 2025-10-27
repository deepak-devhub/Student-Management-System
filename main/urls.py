from django.urls import path

from main import views



urlpatterns = [

    

    path('',views.login),
    path('register',views.register),
    
    path('login',views.login_function, name= 'login'),
    path('register_logic',views.register_logic, name= 'register_logic'),


    # ////////admin side /////


    path('admin-dash',views.admindash, name='admin-dash'),
    path('admin_add_dept',views.admin_add_dept, name='admin_add_dept'),
    path('admin_delete_dept/<int:id>',views.admin_delete_dept, name= 'admin_delete_dept'),
    path('admin_accpt_std/<int:id>',views.admin_accpt_std, name= 'admin_accpt_std'),
    path('admin_rjct_std/<int:id>',views.admin_rjct_std, name= 'admin_rjct_std'),


# //////teacher side //////


    path('teacher-dash',views.teacherdash, name='teacher-dash'),
    path('teacher_profile_update/<int:id>',views.teacher_profile_update, name='teacher_profile_update'),


# /////////student sidee //////

    path('student-dash',views.studentdash, name='student-dash'),
    path('student-update-prof/<int:id>',views.studentupdateprof, name='student-update-prof'),



    path('logout',views.logout, name='logout'),






]
