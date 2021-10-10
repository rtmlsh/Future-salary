import numpy


def predict_salary(payment_from, payment_to, predicted_salaries):
    if payment_from == 0 and payment_to == 0:
        None
    elif payment_from and payment_to:
        predicted_salaries.append(numpy.mean([payment_from, payment_to]))
    elif payment_from:
        predicted_salaries.append(payment_from * 1.2)
    else:
        predicted_salaries.append(payment_to * 0.8)
