.. image:: https://travis-ci.com/molitoris/qr_payment_slip.svg?branch=master
    :target: https://travis-ci.com/molitoris/qr_payment_slip

===============
QR payment slip
===============
QR payment slip generates payment slips for Switzerland and Lichtenstein according to the 'Swiss Payment Standards 2019 (Version 2.1) <https://www.paymentstandards.ch/>'.

Features
--------

- Generates QR payment slip according to Swiss Payment Standard 2019 (Version 2.1)
- Supported output formats
   - SVG
- Supported paper formats
   - A4 containing payment slip (210mm x 297mm)
   - Payment slip only (210mm x 105mm)
- Validates IBAN number & QR reference
- Missing information is replaced by boxes (see samples)

Samples
-------
A selection of payment slips is stored in the `./samples` folder.

Getting Started
---------------
QR payment slip can be installed directly from the Python package index using the `pip` command:

	$ pip install qr-payment-slip

The following example shows how to create a QR payment slip. First an instance of QRPaymentSlip is created and then the
IBAN number, the creditor, the amount and then the debtor is defined. Finally the QR invoice is generated and saved.

.. code-block:: python

    from qr_payment_slip.bill import QRPaymentSlip, Address

    payment_slip = QRPaymentSlip()

    # Set IBAN number (mandatory)
    payment_slip.account = "CH98 8914 4356 9664 7581 5"

    # Set address of creditor (mandatory)
    payment_slip.creditor = Address(name="Hans Muster", address_line_1="Musterstrasse", address_line_2="1",
                                    pcode=1000, town="Musterhausen")

    # Set amount (optional)
    payment_slip.amount = 100

    # Set address of debtor (optional)
    payment_slip.debtor = Address(name="Marie de Brisay", address_line_1="Dreibündenstrasse 34", pcode=7260,
                                  town="Davos Dorf")

    # Generate and save qr payment slip
    payment_slip.save_as("my_bill.svg")

