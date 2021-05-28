from django.http.response import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
import random
import datetime

from finance_project.logger import log
from .forms import NewUserForm, LoginUserForm, OtpVerifyForm, AddBankDetailsForm
from .models import UserDetails, UserBankDetails


# Create your views here.
def home_view(request):
    log.debug("Entering into the function home_view of userapp/views.py")
    log.debug("Method name is "+str(request.method))
    if request.session.get('name') == None:
        request.session['name'] = None
    for k, v in request.session.items():
        log.debug(str(k) + " --> " + str(v))
    context = {'request' : request}

    log.debug("Exiting from the function home_view of userapp/views.py")
    return render(request, 'userapp/home.html', context)
    #return render(request, template_name='userapp/home.html', content_type=context)


def register_view(request):
    log.debug("Entering into the function register_view of userapp/views.py")
    log.debug("Method name is "+str(request.method))

    ## POST request
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        log.debug("request.POST is "+str(request.POST))
        log.debug("Form is bound or not "+str(form.is_bound))
        if form.is_valid():
            log.debug('data is '+str(form.cleaned_data))
            otp = random.randrange(11111, 99999)
            log.debug("OTP is "+ str(otp))
            cdate = datetime.date.today()
            log.debug("cdate "+str(cdate))
            rs_all = UserDetails.objects.all()
            idd = 'U' + str(len(rs_all))
            user_obj = UserDetails(
                cust_id = idd,
                name = form.cleaned_data['name'],
                email = form.cleaned_data['email'],
                telephone = form.cleaned_data['contact'],
                #username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'],
                otp = otp,
                isAuthorized = 0,
                creation_date = datetime.date(cdate.year, cdate.month, cdate.day)
            )

            ## before saving check that email should be present in the database
            screen_email = form.cleaned_data.get('email')
            rs = UserDetails.objects.filter(email__iexact = screen_email)
            if len(rs) > 0:
                log.warning("Email is already registered in the database")
                return HttpResponse("Email is already registered in the database")
            else:
                user_obj.save()
                log.info("Your account has been created! You are now able to log in")
            
            ### send email with otp


            return redirect('/user/login')
        else:
            log.debug("Form is not valid "+ str(form.errors.as_data))
    elif request.method == 'GET':
        #log.debug()
        form = NewUserForm()


    log.debug("Exiting from the function register_view of userapp/views.py")
    return render(request, 'userapp/register.html', {'form' : form})


def login_view(request):
    log.debug("Entering into the function login_view of userapp/views.py")
    log.debug("Method name is "+str(request.method))
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        
        if form.is_valid():
            log.debug("form is valid in login_view")
            screen_email = form.cleaned_data.get('email')
            screen_password = form.cleaned_data.get('password')
            log.info("Screen Credentials " + str(screen_email) + " " + str(screen_password))
            rs = UserDetails.objects.filter(email__iexact = screen_email, password__exact = screen_password)
            if len(rs) == 0:
                log.warning("Invalid Credentials")
            else:
                request.session['email'] = rs[0].email
                if rs[0].isAuthorized == 0:
                    request.session['otp'] = rs[0].otp
                    form = OtpVerifyForm(initial={'email' : screen_email})
                    return render(request, 'userapp/otpverify.html', {'form' : form})
                else:
                    request.session['name'] = rs[0].name
                    request.session['cust_id'] = rs[0].cust_id
                    return redirect('/user')

        else:
            log.warning("form is not valid in login_view")
            pass
    elif request.method == 'GET':
        form = LoginUserForm()
    else:
        pass


    log.debug("Exiting from the function login_view of userapp/views.py")
    return render(request, 'userapp/login.html', {'form' : form})

def logout_view(request):
    log.debug("Entering into the function logout_view of userapp/views.py")
    logout(request)

    for key, val in request.session.items():
        log.debug("Key value pair in logout_request:session is "+str(key)+" "+ str(val))
    log.debug("You have successfully logged out!!") 
    log.debug("Exiting from the function logout_view of userapp/views.py")
    return redirect('/user')


def otpVerify_view(request):
    log.debug("Entering into the function otpverify_view of userapp/views.py")
    log.debug("Method name is "+str(request.method))
    if request.method == 'POST':
        form = OtpVerifyForm(request.POST)
        log.debug(str(request.POST))
        log.debug("Form is :- "+ str(form))
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if otp == request.session.get('otp'):
                log.debug("OTP is verified" + str(form.cleaned_data))
                rs = UserDetails.objects.filter(email__iexact = request.session.get('email'))
                log.debug(str(rs) + str(len(rs)) + str(type(rs)))
                obj = rs[0]
                log.debug("obj values "+ str(obj))
                obj.isAuthorized = 1
                obj.save()
                return redirect('/user/login')
            else:
                log.debug("OTP is wrong")
        else:
            log.debug("Form is not valid")
    else:
        log.debug("method is not post")
        form = OtpVerifyForm()


    log.debug("Exiting from the function otpverify_view of userapp/views.py")
    return render(request, "userapp/otpverify.html", {'form' : form})




def addBank_view(request):
    log.debug("Entering into the function addBank_view of userapp/views.py")
    log.debug("Method name is "+str(request.method))

    if request.method == 'POST':
        form = AddBankDetailsForm(request.POST)
        if form.is_valid():
            log.debug("AddBankDetailsform is valid")
            cust_id_id = request.session.get('cust_id')
            bank = form.cleaned_data.get('bank')
            accountNo = form.cleaned_data.get('accountNo')
            account_type = form.cleaned_data.get('account_type')
            obj = UserBankDetails(
                bank = bank,
                accountNo = accountNo,
                cust_id_id = cust_id_id,
                account_type = account_type
            )

            log.info('Saving the Bank Account Details')
            obj.save()
            form1 = AddBankDetailsForm()
            return render(request, 'userapp/addbank.html', {'form' : form1})
        else:
            log.debug("AddBankDetailsform is not valid")
    elif request.method == 'GET':
        form = AddBankDetailsForm()

    log.debug("Exiting from the function addBank_view of userapp/views.py")
    return render(request, 'userapp/addbank.html', {'form' : form})


def uploadTransactions_view(request):
    log.debug("Entering into the function addBank_view of userapp/views.py")
    log.debug("Method name is "+str(request.method))

    if request.method == 'POST':
        pass


    log.debug("Exiting from the function addBank_view of userapp/views.py")