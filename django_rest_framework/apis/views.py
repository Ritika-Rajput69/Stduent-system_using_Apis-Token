from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .serializers import *
from .models import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import generics
from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentForm
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'token': str(refresh.access_token),
                'user_id': user.id,
                'username': user.username
            })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    return render(request, 'login.html')


from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)  # Clear the session data
    return redirect('login')  # Redirect to the login page, replace 'login' with your login URL name


# @permission_classes([IsAuthenticated])
# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             return render(request, 'student_list.html') 
#         #  {'access_token': str(refresh.access_token), 'refresh_token': str(refresh)}
#         else:
#             return render(request, 'login.html', {'error_message': 'Invalid username or password.'})
#     return render(request, 'login.html')



# @api_view(['POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def student_list(request):
    students = Student.objects.all()  # Fetch all students from the database
    student_list = [{'index': index + 1, 'student': student} for index, student in enumerate(students)]
    context = {
        'student_list': student_list,
        'redirect_to_login_immediately': None  # Placeholder, replace with actual logic if needed
    }
    return render(request, 'student_list.html', context)

# def student_list(request):
#     students = Student.objects.all()
#     return render(request, 'student_list.html', {'students': students})

def student_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    return render(request, 'student_detail.html', {'student': student})

def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form': form})

def student_update(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_form.html', {'form': form})

def student_delete(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'student_confirm_delete.html', {'student': student})


# ----------------------mannually token generate------------------------------

@permission_classes([AllowAny])
class RegisterUser(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        
        if not username or not password:
            return Response({'status': 400, 'message': 'Both username and password are required.'})

        
        if User.objects.filter(username=username).exists():
            return Response({'status': 400, 'message': 'Username already exists.'})

       
        user = User.objects.create_user(username=username, password=password)        
        # token = Token.objects.create(user=user)
        refresh = RefreshToken.for_user(user)

        return Response({'status': 200,
                          'message': 'User created successfully.',
                           'refresh': str(refresh),
        'access': str(refresh.access_token),})




@permission_classes([IsAuthenticated])
class StudentAPI(APIView):

    # authentication_classes = [TokenAuthentication]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response({'status': 200, 'payload': serializer.data})

    def post(self, request):              
        serializer = StudentSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went Wrong'})

        serializer.save() 
        return Response({'status': 200, 'payload': serializer.data, 'message': 'Your Data is saved.' })

    def put(self, request, id):
        try: 
            student_obj = Student.objects.get(id=id)
            serializer = StudentSerializer(student_obj, data=request.data)

            if not serializer.is_valid():
                return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went Wrong'})

            serializer.save()            
            return Response({'status': 200, 'payload': serializer.data, 'message': 'Your Data is saved.'})

        except Student.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'message': "Student not found."})
        except Exception as e:
            return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': "Internal Server Error."})

    def patch(self, request, id):
        try: 
            student_obj = Student.objects.get(id=id)
            serializer = StudentSerializer(student_obj, data=request.data, partial=True)

            if not serializer.is_valid():
                return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went Wrong'})

            serializer.save()            
            return Response({'status': 200, 'payload': serializer.data, 'message': 'Your Data is saved.'})

        except Student.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'message': "Student not found."})
        except Exception as e:
            return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': "Internal Server Error."})

    def delete(self, request, id):    
        try: 
            student_obj = Student.objects.get(id=id)
            student_obj.delete()
            return Response({'status': 200, 'message': "Successfully Deleted..."})

        except Student.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'message': "Student not found."})
        except Exception as e:
            return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': "Internal Server Error."})



#------------Use Generic Views ----------------

@permission_classes([IsAuthenticated])
class StudentGeneric(generics.ListAPIView, generics.CreateAPIView):
    
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # permission_classes = [IsAdminUser]




@permission_classes([IsAuthenticated])
class StudentGeneric1(generics.UpdateAPIView, generics.DestroyAPIView):
    
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = "id"


# -----------------------------------------------------------------------------------

''' Step by step i used here all http methods....'''


# @api_view(['GET'])``
# @permission_classes([AllowAny])
# def student_list(request):
#     students = Student.objects.all()
#     serializer = StudentSerializer(students, many=True)
#     return Response({'status' : 200 ,'payload' :serializer.data})



# @api_view(['POST'])
# @permission_classes([AllowAny])
# def post_student(request):              
#         serializer= StudentSerializer(data=request.data)
#         # data = request.data
#         # # serializer= StudentSerializer(data=request.data)

#         # if request.data['age'] < 18:            
#         #     return Response({"error" : 403, 'message' : 'age must be greater than 18'})

#         if not serializer.is_valid():
#             print(serializer.errors)            
#             return Response({'status' : 403, 'errors' : serializer.errors, 'message' : 'Something went Wrong' })
        
#         serializer.save() 

#         return Response({'status' : 200 ,'payload' : serializer.data, 'message' : 'Your Data is saved.' })


# @api_view(['POST'])  
# #"PUT" to enter complete data. 
# #"PATCH" for partial data.
# @permission_classes([AllowAny])
# def update_student(request,id):

#     try : 
#         student_obj= Student.objects.get(id=id)
        
#         serializer= StudentSerializer(student_obj, data=request.data, partial = True)

#         if not serializer.is_valid():
#             print(serializer.errors)
#             return Response({'status' : 403, 'errors' : serializer.errors, 'message' : 'Something went Wrong' })
        
#         serializer.save()            
#         return Response({'status' : 200 ,'payload' : serializer.data, 'message' : 'Your Data is saved.' })

#     except Exception as e :
#          print(e)
#          return Response({'status' : 403, 'message' : "Invalid id "})
      


# @api_view(['DELETE'])
# @permission_classes([AllowAny])
# def delete_student(request,id):    
    
#     try : 
#         student_obj= Student.objects.get(id=id)
#         student_obj.delete()
#         return Response({'status' : 200, 'message' : "Successfully Deleted..."})

    
#     except Exception as e :
#          return Response({'status' : 403, 'message' : "Invalid id "})
          
    
