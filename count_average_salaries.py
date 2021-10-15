import numpy


def predict_salary(payment_from, payment_to):
    if not payment_from and not payment_to:
        return None
    elif payment_from and payment_to:
        return numpy.mean([payment_from, payment_to])
    elif payment_from:
        return payment_from * 1.2
    else:
        return payment_to * 0.8
