import unittest

from app.exceptions.http_exceptions import APIException
from app.models.bill import Bill
from app.services.backoffice.bill import BillService


class Result:
    def __init__(self, value):
        self.value = value

    def scalar_one_or_none(self):
        return self.value


class Database:
    def __init__(self, bill):
        self.bill = bill

    async def execute(self, _):
        return Result(self.bill)


class BackofficeBillServiceTest(unittest.IsolatedAsyncioTestCase):
    async def test_patient_online_payment_cannot_be_collected_again(self):
        bill = Bill(id=1, patient_id=2, appointment_id=3, amount=100)
        bill.status = "paid"
        bill.paid_by_type = "patient"

        with self.assertRaisesRegex(APIException, "Patient already paid online"):
            await BillService.settle_bill(Database(bill), 1, 4)


if __name__ == "__main__":
    unittest.main()
