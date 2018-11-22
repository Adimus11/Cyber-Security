from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class BankUser(AbstractUser):
    email = models.EmailField(blank=False, unique=True)
    balance = models.FloatField(default=0.0)
    available_founds = models.FloatField(default=0.0)

    def is_sender(self, transfer):
        return self == transfer.sender


class Transfer(models.Model):

    amount = models.FloatField(default=0)
    is_staged = models.BooleanField(default=True)
    sender = models.ForeignKey(BankUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(BankUser, on_delete=models.CASCADE, related_name='receiver')
    date = models.DateTimeField(default=None, null=True)

    def accept(self):
        if self.amount <= self.sender.balance:
            self.sender.balance -= self.amount
            self.receiver.balance += self.amount
            self.is_staged = False
            self.sender.save()
            self.receiver.save()
            self.date = datetime.now()
            self.save()
        else:
            raise Exception

    def delete(self):
        self.sender.available_founds += self.amount
        self.sender.save()
        super(Transfer, self).delete()