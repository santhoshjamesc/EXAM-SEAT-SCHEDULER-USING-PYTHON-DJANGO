"""web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from webapp.views import *
from django.conf import settings
from webapp.views import display_presets, fetch_rooms
from django.conf import settings
from django.conf.urls.static import static


from webapp import views 
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),


   
    path('change-password/', views.change_password, name='change_password'),
    path('delstudents/<int:pk>/', views.delete_student, name='delete_student'),
    path('editstudents/<int:pk>/', views.edit_student, name='edit_student'),
    path('allocate-seats/', views.seat_allocation, name='allocate-seats'),
    path('get-dropdown-data/', views.get_dropdown_data, name='get_dropdown_data'),
    path('', views.home, name='home'),  # Redirect root to home
    path('signin/', views.signin, name='signin'),
    path('search/', views.search_results, name='search_results'),
    path('delete-preset/', delete_preset, name='delete_preset'),
    path('add-students//', views.student_add, name='student_add'),

    path('collect_data/', views.collect_data, name='collect_data'),

    path('search_result/', views.search_results, name='search_results'),

    path('increment_semester/', views.increment_semester, name='increment_semester'),
   
    path('uploadfile/', upload_file, name='upload_file'),
    path('signout/', views.signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    path('students/', views.student_list_and_add, name='student_list_and_add'),  # Corrected URL for student add/list
   
    path('presets/', views.display_presets, name='display_presets'),
    path('rooms/', views.fetch_rooms, name='fetch_rooms'),
    path('seat-allocation/', views.seat_allocation, name='seat_allocation'),
    path('insert_room_details/', views.insert_room_details, name='insert_room_details'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)