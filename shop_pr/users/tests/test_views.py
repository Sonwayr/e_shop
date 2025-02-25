from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from users.models import Address

User = get_user_model()


class UserViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            email="G2BZG@example.com",
            first_name="John",
            last_name="Doe",
            phone_number="1234567890",
        )
        self.admin_user = User.objects.create_superuser(username="admin", password="admin123")

    def test_register_user(self):
        url = reverse("users:register")
        response = self.client.post(url, {
            "username": "newuser",
            "email": "nL2cK@example.com",
            "password1": "Testpass123",
            "password2": "Testpass123",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "1234567890"
        })
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login_user(self):
        url = reverse("users:login")
        response = self.client.post(url, {"username": "testuser", "password": "password123"})
        self.assertEqual(response.status_code, 302)

    def test_profile_view_requires_authentication(self):
        url = reverse("users:profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_edit_profile_view(self):
        self.client.login(username="testuser", password="password123")
        url = reverse("users:edit_profile")
        response = self.client.post(url, {
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "1234567890"
        })
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.phone_number, "1234567890")


class UserAPIViewsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.admin_client = APIClient()
        self.admin_user = User.objects.create_superuser(username="admin", password="admin123")

        self.admin_client.force_authenticate(user=self.admin_user)

    def test_get_user_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("users:user-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["username"], "testuser")

    def test_create_user_fails_when_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse("users:user-list"), {
            "username": "anotheruser",
            "password": "testpassword"
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_user(self):
        url = reverse("users:admin-detail", kwargs={"pk": self.user.pk})
        response = self.admin_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_non_admin_cannot_delete_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("users:admin-detail", kwargs={"pk": self.user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AddressModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.address = Address.objects.create(
            user=self.user,
            street="Main Street",
            house_number="10A",
            city="Berlin",
            country="Germany",
            zip_code="10115"
        )

    def test_address_str(self):
        expected_str = "Main Street, 10A, Berlin, Germany"
        self.assertEqual(str(self.address), expected_str)
