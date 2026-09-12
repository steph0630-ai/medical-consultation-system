import unittest

from app.exceptions.http_exceptions import APIException
from app.models.prescription import Prescription
from app.services.client.prescription import update_item_selection


class Result:
    def __init__(self, value):
        self.value = value

    def scalar_one_or_none(self):
        return self.value


class Database:
    async def execute(self, _):
        return Result(Prescription(id=1, appointment_id=2, doctor_id=3, status="dispensed"))


class ClientPrescriptionServiceTest(unittest.IsolatedAsyncioTestCase):
    async def test_dispensed_prescription_selection_is_locked(self):
        with self.assertRaisesRegex(APIException, "Prescription already dispensed"):
            await update_item_selection(Database(), 1, 1, 1, False)


if __name__ == "__main__":
    unittest.main()
