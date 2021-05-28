from django.db import models
from finance_project.logger import log
# Create your models here.

class UserDetails(models.Model):
    log.debug("Loading UserDetails class of userapp/models.py")
    


    cust_id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length = 40)
    email = models.EmailField(max_length = 100, unique=True)
    telephone = models.CharField(max_length = 10)
    username = models.CharField(max_length=20, null=True)
    password = models.CharField(max_length = 20)
    otp = models.IntegerField()
    isAuthorized = models.IntegerField()
    last_updated_date = models.DateField(auto_now=True)
    creation_date = models.DateField()

    
    
    def __str__ (self):
        return self.name


class UserBankDetails(models.Model):
    log.debug("Loading UserBankDetails class of userapp/models.py")

    cust_id = models.ForeignKey(UserDetails,to_field='cust_id', on_delete=models.CASCADE)
    accountNo = models.CharField(max_length=16)

    BANK_CHOICES = (
        ('hdfc', 'HDFC'),
        ('icici', 'ICICI'),
        ('kotak', 'Kotak Mahindra'),
        ('pnb', 'PNB'),
        ('bob', 'Bank Of Badora'),
        ('sbi', 'SBI'),
        ('paytm', 'Paytm'),
        ('other', 'Other')
    )

    bank = models.CharField(max_length=30, choices=BANK_CHOICES)

    ACCOUNT_CHOICES = (
        ('cur', 'Current'),
        ('sal', 'Salary'),
        ('sav', 'Savings')
    )

    account_type = models.CharField(max_length=30, choices=ACCOUNT_CHOICES)

    def __str__(self):
        return self.bank
    





"""
Optimizing production for a large foreign Thermal Power Plant

• Cleaned & merged sensors data received from thermal plant

• Developed framework for extracting Steady State data from raw data

• Performed EDA and Descriptive Statistics on raw & steady data for feature selection

• Built predictive models for predicting various parameters using sensor data

• Developed several Machine Learning Models like Linear Regression, KNNRegressor, RandomForestRegressor, XgboostRegressor for best fit

• Performed Optimization to increase the production of Electricity.
"""