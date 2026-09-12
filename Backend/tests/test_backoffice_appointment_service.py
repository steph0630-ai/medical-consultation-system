import unittest

from app.exceptions.http_exceptions import APIException
from app.models.appointment import Appointment
from app.schemas.backoffice.appointment import AppointmentUpdate
from app.services.backoffice.appointment import AppointmentService


class Result:
    def __init__(self, value):
        self.value = value

    def scalar_one_or_none(self):
        return self.value


class Database:
    def __init__(self, appointment):
        self.appointment = appointment

    async def execute(self, _):
        return Result(self.appointment)


class BackofficeAppointmentServiceTest(unittest.IsolatedAsyncioTestCase):
    async def test_completed_appointment_is_terminal(self):
        appointment = Appointment(id=1, doctor_id=2, patient_id=3, department_id=4)
        appointment.status = "completed"

        with self.assertRaisesRegex(APIException, "Appointment already completed"):
            await AppointmentService.update_appointment_status(
                Database(appointment),
                doctor_id=2,
                appointment_id=1,
                update_data=AppointmentUpdate(status="confirmed"),
            )


if __name__ == "__main__":
    unittest.main()
