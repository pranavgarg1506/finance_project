from finance_project.logger import log
from django import forms


class NewUserForm(forms.Form):
    log.debug("Loading the NewUserForm class of userapp/forms.py")

    name = forms.CharField(label = 'Name', required=True)
    email = forms.EmailField(label = 'Email', required = True)
    contact = forms.CharField(label = 'Contact', required = True)
    ##username = forms.CharField(label = 'Username', required = True)
    password1 = forms.CharField(label = 'Password', required = True, widget = forms.PasswordInput)
    password2 = forms.CharField(label = 'Password (Again)', required = True, widget = forms.PasswordInput)

    def clean(self):
        log.debug("calling clean method of NewUserForm class of userapp/forms.py "+str(self))

        ## calling clean method of super class to validate
        cleaned_data = super().clean()

        pass1 = cleaned_data.get('password1')
        pass2 = cleaned_data.get('password2')

        if len(pass1) <= 8:
            raise forms.ValidationError('Password should be more than 8 characters')

        if pass1 != pass2:
            raise forms.ValidationError('Passwords do not match')

    def is_valid(self) -> bool:
        log.debug("calling the is_valid function of the NewUserForm class of userapp/forms.py")
        return super().is_valid()

class LoginUserForm(forms.Form):
    log.debug("Loading the NewUserForm class of userapp/forms.py")
    email = forms.CharField(label = 'Email')
    password = forms.CharField(label = 'Password', required = True, widget = forms.PasswordInput)

class OtpVerifyForm(forms.Form):
    log.debug("Loading the OtpVerifyForm class of userapp/forms.py")
    email = forms.CharField(disabled=True, required=False)
    otp = forms.IntegerField()

class AddBankDetailsForm(forms.Form):
    log.debug("Loading the AddBankDetails class of userapp/forms.py")
    accountNo = forms.CharField(max_length=16)

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

    bank = forms.ChoiceField(choices=BANK_CHOICES)
    
    ACCOUNT_CHOICES = (
        ('cur', 'Current'),
        ('sal', 'Salary'),
        ('sav', 'Savings')
    )

    account_type = forms.ChoiceField(choices=ACCOUNT_CHOICES)



class UploadTransactionsForm(forms.Form):
    log.debug("Loading the UploadTransactionsForm class of userapp/forms.py")
