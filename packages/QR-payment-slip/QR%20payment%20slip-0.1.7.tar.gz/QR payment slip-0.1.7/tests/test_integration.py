import pathlib
import unittest

from qr_payment_slip import QRPaymentSlip
from qr_payment_slip.address import Address


class TestQRBillIntegration(unittest.TestCase):

    def test_bill_generation(self):
        my_bill = QRPaymentSlip(
            account="CH9889144356966475815",
            creditor=Address(name="Hans Muster", address_line_1="Musterstrasse 1", pcode=1000, town="Musterhausen"),
        )

        # __file__

        local_dir = pathlib.Path(__file__).parent

        # my_bill.printer.as_sample = True

        my_bill.save_as(local_dir / "../sample/01_bill_minimal.svg")

        my_bill.amount = 1000
        my_bill.save_as(local_dir / "../sample/02_bill_amount.svg")

        my_bill.debtor = Address(name="Marie de Brisay", address_line_1="Dreibündenstrasse 34",
                                 pcode=7260, town="Davos Dorf")
        my_bill.save_as(local_dir / "../sample/03_bill_amount_debtor.svg")

        my_bill.ref_number = "00 00000 00000 00000 00012 34565"
        my_bill.save_as(local_dir / "../sample/04_bill_amount_debtor_ref.svg")

        my_bill.unstructured_message = "Zahlbar bis: 20.01.2020"
        my_bill.save_as(local_dir / "../sample/05_bill_amount_debtor_ref_msg.svg")
