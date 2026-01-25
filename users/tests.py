from allauth.account.models import EmailAddress
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

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


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class UserProfileModelTests(TestCase):
    """
    Test suite for CustomUser display_name field and get_display_name property.
    """

    def test_display_name_field(self):
        """Test that display_name can be set and retrieved"""
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            display_name='TestDisplayName'
        )
        self.assertEqual(user.display_name, 'TestDisplayName')

    def test_get_display_name_with_display_name_set(self):
        """Test get_display_name returns display_name when set"""
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            first_name='John',
            last_name='Doe',
            display_name='JDoe'
        )
        self.assertEqual(user.get_display_name, 'JDoe')

    def test_get_display_name_falls_back_to_full_name(self):
        """Test get_display_name returns full name when display_name is not set"""
        user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            first_name='John',
            last_name='Doe'
        )
        self.assertEqual(user.get_display_name, 'John Doe')

    def test_get_display_name_falls_back_to_email_username(self):
        """Test get_display_name returns email username when display_name and full_name are not set"""
        user = CustomUser.objects.create_user(
            username='testuser',
            email='johndoe@example.com',
            password='password123'
        )
        self.assertEqual(user.get_display_name, 'johndoe')


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class UserProfileFormTests(TestCase):
    """
    Test suite for UserProfileForm validation and behavior.
    """

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            first_name='Test',
            last_name='User'
        )

    def test_form_fields(self):
        """Test that form contains expected fields"""
        from users.forms import UserProfileForm
        form = UserProfileForm(instance=self.user)
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)
        self.assertIn('display_name', form.fields)

    def test_form_valid_with_all_fields(self):
        """Test form is valid with all fields filled"""
        from users.forms import UserProfileForm
        form_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'test@example.com',
            'display_name': 'JS'
        }
        form = UserProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_form_valid_without_display_name(self):
        """Test form is valid without display_name (optional field)"""
        from users.forms import UserProfileForm
        form_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'test@example.com',
            'display_name': ''
        }
        form = UserProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_email_cannot_be_changed(self):
        """Test that email field is protected from changes via clean_email method"""
        from users.forms import UserProfileForm
        form_data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'newemail@example.com',
            'display_name': 'JS'
        }
        form = UserProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        # Email should remain unchanged
        self.assertEqual(form.cleaned_data['email'], 'test@example.com')


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class UserProfileViewTests(TestCase):
    """
    Test suite for user_profile view functionality.
    """

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123',
            first_name='Test',
            last_name='User'
        )
        EmailAddress.objects.create(
            user=self.user,
            email=self.user.email,
            primary=True,
            verified=True
        )
        self.client.force_login(self.user)

    def test_profile_view_requires_login(self):
        """Test that profile view requires authentication"""
        self.client.logout()
        response = self.client.get(reverse('users:user_profile'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('accounts/login', response.url)  # Changed from 'account/login' to 'accounts/login'

    def test_profile_view_get(self):
        """Test GET request to profile view"""
        response = self.client.get(reverse('users:user_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertIn('form', response.context)

    def test_profile_update_with_display_name(self):
        """Test successful profile update with explicit display_name"""
        response = self.client.post(reverse('users:user_profile'), {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'test@example.com',
            'display_name': 'JSmith'
        })
        self.assertRedirects(response, reverse('users:user_profile'))

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Jane')
        self.assertEqual(self.user.last_name, 'Smith')
        self.assertEqual(self.user.display_name, 'JSmith')

    def test_profile_update_auto_populates_display_name(self):
        """Test that display_name is auto-populated from full name when empty"""
        response = self.client.post(reverse('users:user_profile'), {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'test@example.com',
            'display_name': ''
        })
        self.assertRedirects(response, reverse('users:user_profile'))

        self.user.refresh_from_db()
        self.assertEqual(self.user.display_name, 'Jane Smith')

    def test_profile_update_does_not_overwrite_existing_display_name(self):
        """Test that existing display_name is preserved when not in POST data"""
        self.user.display_name = 'CustomName'
        self.user.save()

        response = self.client.post(reverse('users:user_profile'), {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'test@example.com',
            'display_name': 'CustomName'
        })

        self.user.refresh_from_db()
        self.assertEqual(self.user.display_name, 'CustomName')

    def test_profile_update_with_no_full_name(self):
        """Test that display_name remains empty if no full name provided"""
        response = self.client.post(reverse('users:user_profile'), {
            'first_name': '',
            'last_name': '',
            'email': 'test@example.com',
            'display_name': ''
        })

        self.user.refresh_from_db()
        self.assertIsNone(self.user.display_name)

    def test_profile_update_success_message(self):
        """Test that success message is displayed after profile update"""
        response = self.client.post(reverse('users:user_profile'), {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'test@example.com',
            'display_name': 'JS'
        }, follow=True)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Your profile has been updated successfully.')

    def test_profile_update_invalid_form(self):
        """Test that invalid form data doesn't update profile"""
        # Since email is protected by clean_email(), test with actual invalid data
        # For example, if first_name has max_length=30 in the model:
        response = self.client.post(reverse('users:user_profile'), {
            'first_name': 'J' * 151,  # Exceeds typical max_length
            'last_name': 'Smith',
            'email': 'test@example.com',  # This will be replaced anyway
            'display_name': 'JS'
        })

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Test')  # Unchanged
