from allauth.account.models import EmailAddress
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from users.models import CustomUser

"""
The testing framework starts with a clean environment, so we need to override 
storage settings to use the default file system storage backend for testing purposes.
Otherwise the missing staticfiles manifest entry which occurs when using Whitenoise 
with manifest-based storage would result in an error during test execution.
"""


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class CustomUserModelTests(TestCase):
    """
    Test suite for CustomUser model, including custom user creation,
    superuser creation, and data consent date field.
    """

    def test_create_user(self):
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            first_name='Test',
            last_name='User'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        user = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password123'
        )
        self.assertEqual(user.email, 'admin@example.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_data_consent_date(self):
        now = timezone.now().date()
        user = CustomUser.objects.create_user(
            username='consentuser',
            email='consent@example.com',
            password='password123',
            data_consent_date=now
        )
        self.assertEqual(user.data_consent_date, now)


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class UserAuthenticationTests(TestCase):
    """
    Test suite for user authentication, including login functionality
    and email verification.
    """

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        # For mandatory email verification, we need to mark the email as verified
        # for some login tests if they depend on it.
        EmailAddress.objects.create(
            user=self.user,
            email=self.user.email,
            primary=True,
            verified=True
        )

    def test_login_successful(self):
        response = self.client.post(reverse('account_login'), {
            'login': 'test@example.com',
            'password': 'password123'
        })
        self.assertRedirects(response, reverse('core:home'))
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_invalid_password(self):
        response = self.client.post(reverse('account_login'), {
            'login': 'test@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_logout(self):
        self.client.login(email='test@example.com', password='password123')
        response = self.client.post(reverse('account_logout'))
        self.assertRedirects(response, reverse('core:home'))
        self.assertFalse('_auth_user_id' in self.client.session)


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class UserRegistrationTests(TestCase):
    """
    Test suite for user registration, including successful signup,
    duplicate email handling, and email verification.
    """

    def test_signup_successful(self):
        response = self.client.post(reverse('account_signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!'
        })
        # Check if user was created
        self.assertTrue(CustomUser.objects.filter(email='newuser@example.com').exists())
        # With mandatory verification, it should redirect to email verification sent page
        self.assertRedirects(response, reverse('account_email_verification_sent'))
        # Verify verification email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Confirm Your Email Address", mail.outbox[0].subject)

    def test_signup_duplicate_email(self):
        CustomUser.objects.create_user(
            username='existing',
            email='test@example.com',
            password='password123'
        )
        response = self.client.post(reverse('account_signup'), {
            'email': 'test@example.com',
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        # User count should still be 1
        self.assertEqual(CustomUser.objects.filter(email='test@example.com').count(), 1)


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class EmailTests(TestCase):
    """
    Test suite for email functionality, including password reset emails.
    """

    def test_password_reset_sends_email(self):
        CustomUser.objects.create_user(username='testuser', email='test@example.com', password='password123')

        # Trigger the allauth password reset view
        response = self.client.post(reverse('account_reset_password'), {'email': 'test@example.com'})

        # Verify one email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Verify the subject and recipient
        self.assertIn("Password Reset", mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].to, ['test@example.com'])
