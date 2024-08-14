#!/usr/bin/env python3

class TestRegistrationForm(unittest.TestCase):
    def setUp(self):
        self.form = RegistrationForm()

    def test_fields_exist(self):
        self.assertTrue(hasattr(self.form, 'username'))
        self.assertTrue(hasattr(self.form, 'email'))
        self.assertTrue(hasattr(self.form, 'password'))
        self.assertTrue(hasattr(self.form, 'confirm_password'))
        self.assertTrue(hasattr(self.form, 'submit'))

    def test_valid_data(self):
        form = RegistrationForm(username="TestUser", email="test@example.com", password="password", confirm_password="password")
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        form = RegistrationForm(username="", email="invalid", password="pass", confirm_password="different")
        self.assertFalse(form.validate())

    def test_validate_username(self):
        with self.assertRaises(ValidationError):
            self.form.validate_username(username=type('obj', (object,), {'data': 'existing_user'}))

    def test_validate_email(self):
        with self.assertRaises(ValidationError):
            self.form.validate_email(email=type('obj', (object,), {'data': 'existing@example.com'}))

class TestLoginForm(unittest.TestCase):
    def setUp(self):
        self.form = LoginForm()

    def test_fields_exist(self):
        self.assertTrue(hasattr(self.form, 'email'))
        self.assertTrue(hasattr(self.form, 'password'))
        self.assertTrue(hasattr(self.form, 'remember'))
        self.assertTrue(hasattr(self.form, 'submit'))

    def test_valid_data(self):
        form = LoginForm(email="test@example.com", password="password")
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        form = LoginForm(email="invalid", password="")
        self.assertFalse(form.validate())

class TestUpdateAccountForm(unittest.TestCase):
    def setUp(self):
        self.form = UpdateAccountForm()

    def test_fields_exist(self):
        self.assertTrue(hasattr(self.form, 'username'))
        self.assertTrue(hasattr(self.form, 'email'))
        self.assertTrue(hasattr(self.form, 'picture'))
        self.assertTrue(hasattr(self.form, 'submit'))

    def test_valid_data(self):
        form = UpdateAccountForm(username="TestUser", email="test@example.com")
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        form = UpdateAccountForm(username="", email="invalid")
        self.assertFalse(form.validate())

    def test_validate_username(self):
        with self.assertRaises(ValidationError):
            self.form.validate_username(username=type('obj', (object,), {'data': 'existing_user'}))

    def test_validate_email(self):
        with self.assertRaises(ValidationError):
            self.form.validate_email(email=type('obj', (object,), {'data': 'existing@example.com'}))

class TestRequestResetForm(unittest.TestCase):
    def setUp(self):
        self.form = RequestResetForm()

    def test_fields_exist(self):
        self.assertTrue(hasattr(self.form, 'email'))
        self.assertTrue(hasattr(self.form, 'submit'))

    def test_valid_data(self):
        form = RequestResetForm(email="test@example.com")
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        form = RequestResetForm(email="invalid")
        self.assertFalse(form.validate())

    def test_validate_email(self):
        with self.assertRaises(ValidationError):
            self.form.validate_email(email=type('obj', (object,), {'data': 'nonexistent@example.com'}))

class TestResetPasswordForm(unittest.TestCase):
    def setUp(self):
        self.form = ResetPasswordForm()

    def test_fields_exist(self):
        self.assertTrue(hasattr(self.form, 'password'))
        self.assertTrue(hasattr(self.form, 'confirm_password'))
        self.assertTrue(hasattr(self.form, 'submit'))

    def test_valid_data(self):
        form = ResetPasswordForm(password="password", confirm_password="password")
        self.assertTrue(form.validate())

    def test_invalid_data(self):
        form = ResetPasswordForm(password="pass", confirm_password="different")
        self.assertFalse(form.validate())

if __name__ == '__main__':
    unittest.main()
