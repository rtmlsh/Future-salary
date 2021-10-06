import numpy


def predict_salary_hh(currency, payment_from, payment_to, predictioned_salaries):
    if currency != 'RUR':
        None
    elif payment_from == 0 and payment_to == 0:
        None
    elif payment_from and payment_to:
        predictioned_salaries.append(numpy.mean([payment_from, payment_to]))
    elif payment_from:
        predictioned_salaries.append(payment_from * 1.2)
    else:
        predictioned_salaries.append(payment_to * 0.8)


def predict_salary_sj(currency, payment_from, payment_to, predictioned_salaries):
    if currency != 'rub':
        None
    elif payment_from == 0 and payment_to == 0:
        None
    elif payment_from and payment_to:
        predictioned_salaries.append(numpy.mean([payment_from, payment_to]))
    elif payment_from:
        predictioned_salaries.append(payment_from * 1.2)
    else:
        predictioned_salaries.append(payment_to * 0.8)