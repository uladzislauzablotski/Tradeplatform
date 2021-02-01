import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model


@pytest.mark.django_db
class TestUserRegistration():

    User = get_user_model()

    @pytest.mark.parametrize(
        'email, username, password, status_code', [
            ('', '', '', 400),
            ('uladzislau.zablotski@gmail.com', '', '', 400),
            ('uladzislau.zablotski@gmail.com', 'Uladzislau', '', 400),
            ('uladzislau.zablotski@gmail.com', '', 'just_password', 400),
            ('', 'Uladzislau', '', 400),
            ('', '', 'just_password', 400),
            ('', 'Uladzislau', 'just_password', 400),
            ('uladzislau.zablotski@gmail.com', 'Uladzislau', 'just_password', 201),
        ]
    )
    def test_registration_data_validation(self, email, username, password, status_code, api_client):
        url = reverse("signup-list")

        data = {
            'email': email,
            'username': username,
            'password': password,
        }

        response = api_client.post(url, data=data)

        assert response.status_code == status_code

    @pytest.mark.parametrize(
        'email, username, password', [
            ('uladzislau.zablotski@gmail.com', 'Uladzislau', 'just_password'),
            ('test.zablotski@gmail.com', 'Valentin', 'just_password'),
            ('hhh1122@gmail.com', 'Sasha', 'just_password'),
            ('dmitry.matsulevich@gmail.com', 'Dmitry', 'just_password'),
        ]
    )
    def test_creation_of_multiple_users(self, email, username, password, api_client):
        url = reverse("signup-list")

        data = {
            'email': email,
            'username': username,
            'password': password,
        }

        response = api_client.post(url, data=data)
        user = self.User.objects.filter(email=email).first()
        print(user.id)


        assert response.status_code == 201




    @pytest.mark.parametrize(
        'email, username, password', [
            ('uladzislau.zablotskiiii@gmail.com', 'Uladzislau', 'just_password'),
        ]
    )
    def test_is_active_registred_user(self, email, username, password, api_client):

        url = reverse("signup-list")

        data = {
            'email': email,
            'username': username,
            'password': password,
        }

        response = api_client.post(url, data=data)

        assert True