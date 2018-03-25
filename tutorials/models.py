from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_save


class FOSS(models.Model):
    class Meta:
        db_table = 'foss'

class TutorialDetail(models.Model):
    expected_submission_date = models.DateField()
    actual_submission_date = models.DateField()
    contributor = models.ForeignKey(User, on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)

    class Meta:
        db_table = 'tutorial_detail'

    @classmethod
    def update_payments_table(cls, sender, instance, **kwargs):
        queryset = cls.objects.filter(contributor=instance.contributor,
                                      is_published=True)
        payment, _ = Payment.objects.get_or_create(contributor=instance.contributor)
        payment.number_of_tutorials = len(queryset)
        payment.save()

class Payment(models.Model):
    AMT = 1000

    contributor =  models.OneToOneField(User, on_delete=models.CASCADE)
    number_of_tutorials = models.IntegerField(default=0)

    @property
    def total_amt(self):
        return self.number_of_tutorials * self.AMT

    class Meta:
        db_table = 'payment'

post_save.connect(TutorialDetail.update_payments_table, sender=TutorialDetail)
