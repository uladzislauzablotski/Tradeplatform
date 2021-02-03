import pytest
from django.urls import reverse
from accounts.scripts import generate_token, get_domain
from django.contrib.auth import get_user_model


@pytest.mark.django_db
class TestUserRegistrationAndActivation:

    User = get_user_model()
    signup_url = reverse("signup-list")

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
        url = self.signup_url

        data = {
            'email': email,
            'username': username,
            'password': password,
        }

        response = api_client.post(url, data=data)

        assert response.status_code == status_code

    @pytest.mark.parametrize(
        'email, username, password', [
            ('uladzislau.zablotskiy@gmail.com', 'Uladzislau', 'just_password'),
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

        user = self.User.objects.filter(email=email)

        assert response.status_code == 201
        assert user.count() == 1


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

        api_client.post(url, data=data)

        is_active = self.User.objects.filter(email=email).first().is_active

        assert is_active == False

    def test_activation_of_user_by_link(self, api_client):
        data = {
            'email': 'hhh111@gmail.com',
            'username': 'vladzimir',
            'password': 'just_password'
        }

        api_client.post(self.signup_url, data=data)

        user = self.User.objects.filter(email=data.get('email')).first()

        token = generate_token(pk=user.pk)
        link = get_domain() + reverse('activate-detail', args=[token])

        response = api_client.get(link)

        assert self.User.objects.get(pk=user.pk).is_active == True
        assert response.status_code == 200

    @pytest.mark.parametrize(
        'token', [
            (str(generate_token(pk=34545, another_field='nothing'))),
            (str(generate_token(pk=100000))),
            (str(generate_token())),

        ]
    )
    def test_activation_of_user_by_invalid_link(self, token, api_client):
        link = reverse('activate-detail', args=[token])

        response = api_client.get(link)

        assert response.status_code == 400

    def test_activation_of_user_by_the_same_link_twice(self, api_client):
        data = {
            'email': '33user@gmail.com',
            'username': 'vladzimir',
            'password': 'just_password'
        }

        api_client.post(self.signup_url, data=data)

        user_id = self.User.objects.filter(email=data.get('email')).first().id

        token = generate_token(pk=user_id)

        link = get_domain() + reverse('activate-detail', args=[token])

        response1 = api_client.get(link)
        response2 = api_client.get(link)

        assert response1.status_code == 200
        assert response2.status_code == 400
    # ---------------------------------------------------------------

@pytest.mark.django_db
class TestAccessibilityEndpoints:

    User = get_user_model()
    signup_url = reverse("signup-list")
    activate_url = get_domain() + "/account/activate/"

    def test_signup_get_request(self, api_client):
        response = api_client.get(self.signup_url)

        assert response.status_code == 405

    def test_signup_post_request(self, api_client):
        data = {
            'email': 'dimahren@gmail.com',
            'username': 'dimahren',
            'password': 'just_password',
        }

        response = api_client.post(self.signup_url, data=data)

        assert response.status_code != 404

    @pytest.mark.parametrize(
        'path', [
            ('1'),
            ('1000'),
            ('hhh'),
            ('fkhsekj23423'),
            ('hhh213_.435')
        ]
    )
    def test_signup_retrieve(self, api_client, path):
        response = api_client.get(self.signup_url + path)

        assert response.status_code == 404

    # ---------------------------------

    def test_activate_get(self, api_client):
        response = api_client.get(self.activate_url)

        assert response.status_code == 404

    @pytest.mark.parametrize(
        'path', [
            ('1'),
            ('1000'),
            ('hhh'),
            ('fkhsekj23423'),
            ('hhh213_.435')
        ]
    )
    def test_activate_retrieve(self, api_client, path):

        response = api_client.get(self.activate_url + path)

        assert response.status_code != 404

    @pytest.mark.parametrize(
        'path', [
            ('1'),
            ('1000'),
            ('hhh'),
            ('fkhsekj23423'),
            ('hhh213_.435')
        ]
    )
    def test_activate_update(self, api_client, path):

        response = api_client.put(self.activate_url + path, data={'user': 'hello'})

        assert response.status_code == 405

    @pytest.mark.parametrize(
        'path', [
            ('1'),
            ('1000'),
            ('hhh'),
            ('fkhsekj23423'),
            ('hhh213_.435')
        ]
    )
    def test_activate_delete(self, api_client, path):

        response = api_client.delete(self.activate_url + path)

        assert response.status_code == 405











