import unittest

from app.exceptions.http_exceptions import APIException
from app.models.appointment import Appointment
from app.services.client.appointment import appointment_service


class Result:
    def __init__(self, value):
        self.value = value

    def scalar_one_or_none(self):
        return self.value


class Database:
    def __init__(self, appointment):
        self.appointment = appointment
        self.calls = 0

    async def execute(self, _):
        self.calls += 1
        return Result(self.appointment)


class AppointmentCancellationTest(unittest.IsolatedAsyncioTestCase):
    async def test_cancellation_rules(self):
        missing = Database(None)
        self.assertFalse(
            await appointment_service.cancel_appointment(missing, 1, 1)
        )

        pending = Database(Appointment(id=1, patient_id=1, status="pending"))
        self.assertTrue(
            await appointment_service.cancel_appointment(pending, 1, 1)
        )
        self.assertEqual(pending.calls, 2)

        confirmed = Database(Appointment(id=1, patient_id=1, status="confirmed"))
        with self.assertRaises(APIException):
            await appointment_service.cancel_appointment(confirmed, 1, 1)


if __name__ == "__main__":
    unittest.main()
