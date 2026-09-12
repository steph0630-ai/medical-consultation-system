import unittest

from app.services.client.triage import _extract_department_names


class TriageServiceTest(unittest.IsolatedAsyncioTestCase):
    async def test_extracts_longest_department_names_in_text_order(self):
        self.assertEqual(
            await _extract_department_names("建议先挂心血管内科，也可考虑骨科。"),
            ["心血管内科", "骨科"],
        )


if __name__ == "__main__":
    unittest.main()
