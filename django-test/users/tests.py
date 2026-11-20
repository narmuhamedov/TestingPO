import tempfile
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import CustomUser


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class UserAuthTests(TestCase):
    GIF = (
        b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04"
        b"\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
    )

    def _photo(self, name='test.gif'):
        return SimpleUploadedFile(name, self.GIF, content_type='image/gif')

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='StrongPassword123',
            phone_number='+996333222111',
            date_bir='2000-01-01',
            gender='MALE',
            city='Bishkek',
            photo=self._photo('user.gif'),
        )

    def test_register(self):
        response = self.client.post('/register/', {
            'username': "newuser",
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123',
            'first_name': 'Ivan',
            'email': 'ivan@gmail.com',
            'phone_number': '+996444222111',
            'date_bir': "1999-05-05",
            'gender': 'MALE',
            'city': 'Tokmok',
            'photo': self._photo('new.gif'),
        })

        if response.status_code == 200 and 'form' in response.context:
            print("FORM ERRORS:", response.context['form'].errors)

        self.assertRedirects(response, '/login/')
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_login_and_profile(self):
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'StrongPassword123'
        })
        self.assertRedirects(response, '/profile/')
        self.assertEqual(self.client.get('/profile/').status_code, 200)

    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.get('/logout/')
        self.assertRedirects(response, '/login/')