import pytest
from django.core.exceptions import ValidationError
from users.models import CustomUser, Address

@pytest.mark.django_db
class TestCustomUser:
    def test_create_user(self):
        user = CustomUser.objects.create_user(username="testuser", password="password123", phone_number="1234567890")
        assert CustomUser.objects.count() == 1
        assert user.username == "testuser"
        assert user.phone_number == "1234567890"

    def test_user_str(self):
        user = CustomUser.objects.create_user(username="testuser", password="password123")
        assert str(user) == "testuser"


@pytest.mark.django_db
class TestAddress:
    def test_create_address(self):
        user = CustomUser.objects.create_user(username="testuser", password="password123")
        address = Address.objects.create(
            user=user,
            street="Main Street",
            house_number="10A",
            city="Berlin",
            country="Germany",
            zip_code="10115"
        )

        assert Address.objects.count() == 1
        assert address.user == user
        assert address.street == "Main Street"
        assert address.house_number == "10A"
        assert address.city == "Berlin"
        assert address.country == "Germany"
        assert address.zip_code == "10115"

    def test_address_str(self):
        user = CustomUser.objects.create_user(username="testuser", password="password123")
        address = Address.objects.create(
            user=user,
            street="Main Street",
            house_number="10A",
            city="Berlin",
            country="Germany",
            zip_code="10115"
        )

        expected_str = "Main Street, 10A, Berlin, Germany"
        assert str(address) == expected_str
