from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Patient, MedicalRecord

class HospitalAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create two users (doctors)
        self.doctor1 = User.objects.create_user(username='doc1', password='pass123')
        self.doctor2 = User.objects.create_user(username='doc2', password='pass456')

        # Login doctor1
        response = self.client.post('/api/login/', {'username': 'doc1', 'password': 'pass123'}, format='json')
        self.token1 = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token1}')

        # Doctor1 creates a patient
        self.patient1 = Patient.objects.create(
            name='John Doe', age=30, gender='Male', address='123 Street', created_by=self.doctor1
        )

        # Add record for patient1
        self.record1 = MedicalRecord.objects.create(
            patient=self.patient1,
            symptoms='Fever',
            diagnosis='Flu',
            treatment='Rest',
        )

    def test_patient_creation(self):
        """Test doctor can create a patient"""
        response = self.client.post('/api/patients/', {
            'name': 'Jane Doe',
            'age': 25,
            'gender': 'Female',
            'address': '456 Avenue'
        }, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'Jane Doe')

    def test_view_own_patients(self):
        """Test doctor sees only their patients"""
        response = self.client.get('/api/patients/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'John Doe')

    def test_restrict_other_doctor_access(self):
        """Test another doctor cannot access other's patient records"""
        # Login as doctor2
        response = self.client.post('/api/login/', {'username': 'doc2', 'password': 'pass456'}, format='json')
        token2 = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token2}')

        # Try to access patient1's records
        response = self.client.get(f'/api/patients/{self.patient1.id}/records/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)  # Should be empty

    def test_login_returns_token(self):
        """Test that login returns access and refresh tokens"""
        response = self.client.post('/api/login/', {'username': 'doc1', 'password': 'pass123'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
