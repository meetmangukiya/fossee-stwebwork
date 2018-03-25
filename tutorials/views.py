import datetime
import re
import logging

from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render

from .models import TutorialDetail
from .models import Payment


def date_from_string(date):
    """
    Parse strings of form YYYY-MM-DD to python ``datetime.date`` objects.
    """
    date_regex = re.compile(r'(\d{4})-(\d{2})-(\d{2})')
    match = date_regex.match(date)
    year, month, day = match.groups()
    return datetime.date(year=int(year), month=int(month), day=int(day))

def statistics(request):
    """
    Show statistics for:
    - all users
    - specified users
    - show payment information or not
    """
    user = request.GET.get('username')
    show_payment = True if request.GET.get('payment') else False
    end_date = (date_from_string(request.GET.get('end_date'))
                    if request.GET.get('end_date') else datetime.date.today())
    start_date = (date_from_string(request.GET.get('start_date'))
                    if request.GET.get('start_date')
                    else (start_date - datetime.timedelta(days=30)))

    users = [User.objects.get(username=user)] if user else User.objects.all()

    logging.warning(start_date, end_date)

    users = {user:
                {'tutorials':
                    TutorialDetail.objects.filter(contributor=user).filter(
                        Q(expected_submission_date__range=[start_date, end_date]) |
                        Q(actual_submission_date__range=[start_date, end_date])),
                 'payment': Payment.objects.get(contributor=user)}
                for user in users}

    return render(request, 'tutorials/statistics.html',
                  {'users': users, 'show_payment': show_payment,
                   'PaymentModel': Payment})
