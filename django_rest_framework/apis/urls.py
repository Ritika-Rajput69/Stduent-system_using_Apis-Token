from django.urls import include, path
from rest_framework import routers
from .views import *
from rest_framework.authtoken import views

'''router.register() method associates a viewset with a URL pattern.

viewsets = -- handle multiple HTTP methods for a particular resource, 
--useful when you have a model or queryset that you want to 
expose via an API and you want to provide CRUD.


routers :- are uti  lity classes that help in automatically
generating URL patterns for views based on the configuration of ViewSets.'''

from .views import *
# router = routers.DefaultRouter()
# router.register(r'geeks', GeeksViewSet)
from django.urls import path
from .views import *
from . import views


urlpatterns = [
	# path('', include(router.urls)),

	
    # path('api-token-auth/', views.obtain_auth_token),
    # path('students/', student_list),
    # path('stu_post_req/',post_student),
    # path('update-student/<id>/', update_student),
    # path('delete-student/<id>', delete_student),


    path('register/', RegisterUser.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('students/', StudentAPI.as_view(), name='student-list'),
    path('students/<int:id>/', StudentAPI.as_view(), name='student-detail'),

    path('generic-student/', StudentGeneric.as_view()),
    path('generic-student/<id>/', StudentGeneric1.as_view()),
    

 
    # path('login/', login_view, name='login'),
    path('login/', login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    
     
    
   
    path('student/', student_list, name='student_list'),
  
    path('student/<int:student_id>/', student_detail, name='student_detail'),
    path('student/create/', student_create, name='student_create'),
    path('student/<int:student_id>/update/', student_update, name='student_update'),
    path('student/<int:student_id>/delete/', student_delete, name='student_delete'),
    path('',StudentAPI.as_view()),

   

   

    


    # path('get-book/' , get_book), 
    # path('students/', student_list, name='student-list'),
    # path('students/create/', create_student, name='student-create'),
    # path('students/<int:id>/update/', update_student, name='student-update'),
    # path('students/<int:id>/delete/', delete_student, name='student-delete'),
    # path('student/', StudentAPI.as_view()),

    
]


