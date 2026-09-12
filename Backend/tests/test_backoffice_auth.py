import unittest

from pydantic import ValidationError

from app.core.security import AuthBase
from app.schemas.backoffice.admin import AdminCreate


class BackofficeAuthTest(unittest.TestCase):
    def test_access_token_scope_and_assignable_roles(self):
        token = AuthBase.create_access_token("1", scope="backoffice")
        self.assertEqual(AuthBase.verify_token(token, scope="backoffice")["sub"], "1")
        self.assertIsNone(AuthBase.verify_token(token, scope="client"))

        AdminCreate(email="admin@example.com", password="admin123", role="superadmin")
        with self.assertRaises(ValidationError):
            AdminCreate(email="doctor@example.com", password="doctor123", role="doctor")


if __name__ == "__main__":
    unittest.main()
