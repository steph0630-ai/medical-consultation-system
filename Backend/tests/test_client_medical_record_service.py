import unittest

from app.services.client.medical_record import MedicalRecordService


class ClientMedicalRecordServiceTest(unittest.IsolatedAsyncioTestCase):
    async def test_query_is_scoped_to_patient(self):
        query = await MedicalRecordService.get_my_records_query(None, 42)
        params = query.compile().params
        self.assertIn(42, params.values())


if __name__ == "__main__":
    unittest.main()
