from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import GeeksModel, Student
from .serializers import GeeksSerializer, StudentSerializer


class GeeksViewSetTestCase(APITestCase):
    
    def test_geeks_list(self):
        url = reverse('geeks-list')  # Assuming you've defined a URL pattern for GeeksViewSet
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add more assertions to test the response data if needed

    def test_geeks_detail(self):
        geek_id = self.geek1.id
        url = reverse('geeks-detail', kwargs={'pk': geek_id})  # Assuming you've defined a URL pattern for GeeksViewSet detail endpoint
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add more assertions to test the response data if needed


class StudentListTestCase(APITestCase):

    def test_student_list(self):
        url = reverse('student-list')  # Assuming you've defined a URL pattern for student_list view
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Add more assertions to test the response data if needed
