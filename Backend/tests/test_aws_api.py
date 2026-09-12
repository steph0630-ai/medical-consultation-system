import unittest
from types import SimpleNamespace

from app.api.client.v1.aws import generate_presigned_download_url
from app.exceptions.http_exceptions import APIException


class AwsApiTest(unittest.IsolatedAsyncioTestCase):
    async def test_download_url_rejects_another_users_file(self):
        with self.assertRaises(APIException) as raised:
            await generate_presigned_download_url(
                file_key="users/8/report.pdf",
                current_user=SimpleNamespace(id=9),
            )
        self.assertEqual(raised.exception.status_code, 403)


if __name__ == "__main__":
    unittest.main()
