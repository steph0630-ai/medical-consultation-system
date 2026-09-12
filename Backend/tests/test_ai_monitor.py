import unittest

from app.api.backoffice.v1.ai_monitor import overview
from app.exceptions.http_exceptions import ValidationError


class AiMonitorApiTest(unittest.IsolatedAsyncioTestCase):
    async def test_overview_rejects_unsupported_days(self):
        with self.assertRaisesRegex(ValidationError, "Days must be one of"):
            await overview(days=8, agent_type=None, db=None, _=None)


if __name__ == "__main__":
    unittest.main()
