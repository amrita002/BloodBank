from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from blood.models import *
from datetime import datetime, date, time
from datetime import timedelta

def index(request):
    template = loader.get_template('index.html')
    context = {  'mess':'', }

    request.session.flush()

    return HttpResponse(template.render(context,request))

def login(request):
    template = loader.get_template('login.html')
    context = {}

    ulobj = Users.objects.all()
    if request.method == 'POST':

        user_mail = request.POST.get('uemail')
        user_pass = request.POST.get('user_pass')

        for x in ulobj:
            if x.user_mail == user_mail and x.user_pass == user_pass:
                request.session['mail'] = user_mail
                request.session['type'] = x.user_role

                if x.user_role == 'customer':
                    return redirect(blood_avai)

                if x.user_role == 'hospital':
                    return redirect(hos_display_blood)

                if x.user_role == 'bank':
                    return redirect(bank_home)

        context['message'] = "Permission denied, email or password in-correct"

    return HttpResponse(template.render(context,request))

def reg(request):
    template = loader.get_template('register.html')
    context = {'mess': ''}
    request.session.flush()
    c = 0
    urobj = Users.objects.all()

    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_mail = request.POST.get('user_mail')
        user_pass = request.POST.get('user_pass')
        user_pass1 = request.POST.get('user_pass1')
        user_phone_number = request.POST.get('user_phone_number')
        user_address = str(request.POST.get('user_address')).title()
        user_role = request.POST.get('user_role')

        if user_pass != user_pass1:
            context['mess'] = ' Password mismatch '

        try:
            user_phone_number == int(user_phone_number)
        except:
            context['mess'] += ' Enter Phone number correctly '

        if context['mess'] == '':
            for x in urobj:

                if x.user_mail == user_mail or x.user_name == user_name:
                    context['mess'] = 'user already exists'
                    c = 1

            if c != 1:
                ucobj = Users.objects.create(
                    user_name=user_name,
                    user_main_branch_name=user_name,
                    user_mail=user_mail,
                    user_pass=user_pass,
                    user_address=user_address,
                    user_phone_number=user_phone_number,
                    user_role=user_role
                )
                ucobj.save()

                if user_role == 'bank':
                    bcobj = Blood_bank.objects.create(
                        mail=user_mail,
                        user_main_branch_name=user_name,
                        location=user_address,
                        bank_name=user_name
                    )
                    bcobj.save()

                context['mess'] = 'Registration Successful'
                return redirect('reg_ack')

    return HttpResponse(template.render(context,request))

def reg_ack(request):
    template = loader.get_template('reg_ack.html')
    context = {}

    return HttpResponse(template.render(context, request))

def logout(request):
    template = loader.get_template('logout.html')
    context = {'mess': ''}
    request.session.flush()

    return redirect('index')

def forgot(request):
    template = loader.get_template('forgot.html')
    context = {'mess': ''}

    if request.method == 'POST':
        sname = request.POST.get('user_name')
        smail = request.POST.get('user_mail')
        spass = request.POST.get('user_pass')

        uobj = Users.objects.all()

        for x in uobj:
            if x.user_mail == smail and x.user_name == sname:
                x.user_pass = spass
                context['mess'] = 'Successfully Password Changed'
                x.save()

        if context['mess'] != 'Successfully Password Changed':
            context['mess'] = 'username or email not found'

    return HttpResponse(template.render(context, request))

def sam(request):
    template = loader.get_template('sam_html.html')
    context = {'mess': ''}

    return HttpResponse(template.render(context,request))

# ------------------ Blood Bank

def bank_home(request):
    template = loader.get_template('bank/bank_home.html')
    context = {'mess': '','bdloc':''}
    context['user_mail'] = user_mail = request.session['mail']
    context['uobj'] = uobj = Users.objects.get(user_mail=user_mail)
    context['urobj'] = urobj = Users.objects.all()

    if uobj.user_main_branch_name == uobj.user_name:
      context['main'] = 'yes'

    id = 0
    location = ''

    ureg = Users.objects.get(user_mail=user_mail)
    context['bdloc'] = ureg.user_name.title()
    context['bobj'] = bobj = Blood_bank.objects.all()

    for x in bobj:
        if x.mail == user_mail:
            id = x.id

    if request.method == 'POST':
        group = request.POST.get('group')
        units = request.POST.get('units')
        bvobj = Blood_bank.objects.get(id=id)

        if group == 'a+':
            bvobj.a_positive += int(units)

        if group == 'b+':
            bvobj.b_positive += int(units)

        if group == 'ab+':
            bvobj.ab_positive += int(units)

        if group == 'o+':
            bvobj.o_positive += int(units)

        if group == 'a-':
            bvobj.a_negative += int(units)

        if group == 'b-':
            bvobj.b_negative += int(units)

        if group == 'ab-':
            bvobj.ab_negative += int(units)

        if group == 'o-':
            bvobj.o_negative += int(units)

        bvobj.save()

        return redirect(bank_home)

    return HttpResponse(template.render(context, request))

def bank_don_req(request):
    template = loader.get_template('bank/bank_don_req.html')
    context = {'mess': '','dis':''}
    c = 0
    context['user_mail'] = user_mail = request.session['mail']
    context['uobj'] = uobj = Users.objects.get(user_mail=user_mail)
    context['urobj'] = urobj = Users.objects.all()
    context['ureg'] = ureg = Users.objects.get(user_mail=user_mail)
    context['uloc'] = ureg.user_address
    context['bobj'] = bobj = Donor_reports.objects.all()
    if uobj.user_main_branch_name == uobj.user_name:
      context['main'] = 'yes'

    bvobj = Blood_bank.objects.get(mail=user_mail)

    for x in bobj:

        if x.status == 'not yet approved' and x.bank_name == uobj.user_name:
            c = 1
            context['dis'] = 'y'

    if c == 0:
        context['dis'] = ''

    if request.method == 'POST':
        selopt = request.POST.get('selopt')
        vstat = request.POST.get('vstat')

        getobj = Donor_reports.objects.get(id=selopt)
        getobj.status = str(vstat)

        if vstat == 'Accepted':
            if getobj.group == 'a+':
                bvobj.a_positive += int(getobj.units)

            if getobj.group == 'b+':
                bvobj.b_positive += int(getobj.units)

            if getobj.group == 'ab+':
                bvobj.ab_positive += int(getobj.units)

            if getobj.group == 'o+':
                bvobj.o_positive += int(getobj.units)

            if getobj.group == 'a-':
                bvobj.a_negative += int(getobj.units)

            if getobj.group == 'b-':
                bvobj.b_negative += int(getobj.units)

            if getobj.group == 'ab-':
                bvobj.ab_negative += int(getobj.units)

            if getobj.group == 'o-':
                bvobj.o_negative += int(getobj.units)

        bvobj.save()
        getobj.save()

        context['mess'] = 'Request Updated'
        return redirect('bankdonreq')

    return HttpResponse(template.render(context, request))

def bank_don_report(request):
    template = loader.get_template('bank/bank_don_report.html')
    context = {'mess': ''}
    context['user_mail'] = user_mail = request.session['mail']
    context['uobj'] = uobj = Users.objects.get(user_mail=user_mail)
    context['urobj'] = urobj = Users.objects.all()

    context['ureg'] = ureg = Users.objects.all()
    rg = 0

    context['bvobj'] = bvobj = Blood_bank.objects.all()
    context['bobj'] = bobj = Donor_reports.objects.all()
    if uobj.user_main_branch_name == uobj.user_name:
      context['main'] = 'yes'

    if request.method == 'POST':

        group = str(request.POST.get('group'))
        location = str(request.POST.get('location')).title()

        for x in bobj:
            rg = 1
            if x.user_location == location and str(x.group) == str(group):
                print(x.user_location, location, group, x.group,x.status,x.bol)
                context['mess'] = 'yes'
                context['bg'] = str(x.group)
                context['bl'] = str(x.user_location)

        if context['mess'] == '' and rg == 1:
            context['rep'] = 'No Results found, please search again'

    return HttpResponse(template.render(context, request))

def bank_hos_req(request):
    template = loader.get_template('bank/bank_hos_req.html')
    context = {'mess': ''}
    context['user_mail'] = user_mail = request.session['mail']
    context['uobj'] = uobj = Users.objects.get(user_mail=user_mail)
    context['urobj'] = urobj = Users.objects.all()

    c,b = 0,0
    context['bsobj'] = bsobj = Blood_seek.objects.all()
    context['bvobj'] = bvobj = Blood_bank.objects.all()

    ureg = Users.objects.get(user_mail=user_mail)
    location = ureg.user_address
    context['location'] = location
    if uobj.user_main_branch_name == uobj.user_name:
      context['main'] = 'yes'

    for x in bsobj:
        if x.role == 'hospital' and x.bank_name == uobj.user_name and x.status == 'not yet approved':
            c = 1
            context['dis'] = 'y'

    if c == 0:
        context['dis'] = ''

    if request.method == 'POST':
        selopt = request.POST.get('selopt')
        vstat = request.POST.get('vstat')
        upobj = Blood_seek.objects.get(id=selopt)
        obj = Blood_bank.objects.get(bank_name=upobj.bank_name)

        if vstat == 'Accepted':
            if upobj.group == 'a+':
                if upobj.units <= obj.a_positive:
                    b = 1
                    obj.a_positive -= int(upobj.units)
            if upobj.group == 'b+':
                if upobj.units <= obj.b_positive:
                    b = 1
                    obj.b_positive -= int(upobj.units)
            if upobj.group == 'ab+':
                if upobj.units <= obj.ab_positive:
                    b = 1
                    obj.ab_positive -= int(upobj.units)
            if upobj.group == 'o+':
                if upobj.units <= obj.o_positive:
                    b = 1
                    obj.o_positive -= int(upobj.units)
            if upobj.group == 'a-':
                if upobj.units <= obj.a_negative:
                    b = 1
                    obj.a_negative -= int(upobj.units)
            if upobj.group == 'b-':
                if upobj.units <= obj.b_negative:
                    b = 1
                    obj.b_negative -= int(upobj.units)
            if upobj.group == 'ab-':
                if upobj.units <= obj.ab_negative:
                    b = 1
                    obj.ab_negative -= int(upobj.units)
            if upobj.group == 'o-':
                if upobj.units <= obj.o_negative:
                    b = 1
                    obj.o_negative -= int(upobj.units)
        else:
            b = 1

        if b == 1:
            if vstat == 'Accepted':
                obj.save()

            upobj.status = vstat
            upobj.save()

            return redirect('bankhosreq')
        else:
            context['mess'] = 'Blood in-sufficent'

    return HttpResponse(template.render(context, request))

def bank_seek_req(request):
    template = loader.get_template('bank/bank_seek_req.html')
    context = {'mess': '','dis':''}
    context['user_mail'] = user_mail = request.session['mail']
    context['uobj'] = uobj = Users.objects.get(user_mail=user_mail)
    context['urobj'] = urobj = Users.objects.all()

    context['bsobj'] = bsobj = Blood_seek.objects.all()
    context['bvobj'] = bvobj = Blood_bank.objects.all()
    context['dis'] = ''
    c, b = 0, 0
    ureg = Users.objects.get(user_mail=user_mail)
    location = ureg.user_address
    context['location'] = location
    context['user_name'] = uobj.user_name
    if uobj.user_main_branch_name == uobj.user_name:
      context['main'] = 'yes'

    for x in bsobj:
        if x.role != 'hospital' and x.bank_name == uobj.user_name and x.status == 'not yet approved':
            c = 1
            context['dis'] = 'y'

    if c == 0:
        context['dis'] = ''

    if request.method == 'POST':
        selopt = request.POST.get('selopt')
        vstat = request.POST.get('vstat')
        upobj = Blood_seek.objects.get(id=selopt)
        obj = Blood_bank.objects.get(bank_name=upobj.bank_name)

        if vstat == 'Accepted':
            if upobj.group == 'a+':
                if upobj.units <= obj.a_positive:
                    b = 1
                    obj.a_positive -= int(upobj.units)
            if upobj.group == 'b+':
                if upobj.units <= obj.b_positive:
                    b = 1
                    obj.b_positive -= int(upobj.units)
            if upobj.group == 'ab+':
                if upobj.units <= obj.ab_positive:
                    b = 1
                    obj.ab_positive -= int(upobj.units)
            if upobj.group == 'o+':
                if upobj.units <= obj.o_positive:
                    b = 1
                    obj.o_positive -= int(upobj.units)
            if upobj.group == 'a-':
                if upobj.units <= obj.a_negative:
                    b = 1
                    obj.a_negative -= int(upobj.units)
            if upobj.group == 'b-':
                if upobj.units <= obj.b_negative:
                    b = 1
                    obj.b_negative -= int(upobj.units)
            if upobj.group == 'ab-':
                if upobj.units <= obj.ab_negative:
                    b = 1
                    obj.ab_negative -= int(upobj.units)
            if upobj.group == 'o-':
                if upobj.units <= obj.o_negative:
                    b = 1
                    obj.o_negative -= int(upobj.units)
        else:
            b = 1

        if b == 1:
            if vstat == 'Accepted':
                obj.save()
            upobj.status = vstat
            upobj.save()
            context['mess'] = 'Request Updated'

            return redirect('bankseekreq')
        else:
            context['mess'] = 'Blood in-sufficent'

    return HttpResponse(template.render(context, request))

def bank_add_branch(request):
    template = loader.get_template('bank/bank_add_bank.html')
    context = {'mess': ''}
    context['user_mail'] = user_mail = request.session['mail']
    context['uobj'] = uobj = Users.objects.get(user_mail=user_mail)
    context['urobj'] = urobj = Users.objects.all()
    c = 0
    if uobj.user_main_branch_name == uobj.user_name:
      context['main'] = 'yes'

    if request.method == 'POST':

        user_mail = request.POST.get('user_mail')
        user_pass = request.POST.get('user_pass')
        user_pass1 = request.POST.get('user_pass1')
        user_phone_number = request.POST.get('user_phone_number')
        user_address = str(request.POST.get('user_address')).title()
        user_role = 'bank'
        user_name = uobj.user_main_branch_name + '_' + str(user_address)

        if user_pass != user_pass1:
            context['mess'] = ' Password mismatch '

        try:
            user_phone_number == int(user_phone_number)
        except:
            context['mess'] += ' Enter Phone number correctly '

        if context['mess'] == '':
            for x in urobj:

                if x.user_mail == user_mail:
                    context['mess'] = 'user already exists'
                    c = 1

                if x.user_name == user_name:
                    context['mess'] = 'branch already exists'
                    c = 1

                if x.user_address == user_address and x.user_main_branch_name ==uobj.user_main_branch_name:
                    context['mess'] = 'branch already exists'
                    c = 1

            if c != 1:
                ucobj = Users.objects.create(
                    user_name=user_name,
                    user_main_branch_name=uobj.user_main_branch_name,
                    user_mail=user_mail,
                    user_pass=user_pass,
                    user_address=user_address,
                    user_phone_number=user_phone_number,
                    user_role=user_role
                )
                ucobj.save()
                bcobj = Blood_bank.objects.create(
                    mail=user_mail,
                    location=user_address,
                    bank_name=user_name,
                    user_main_branch_name=uobj.user_main_branch_name
                )
                bcobj.save()
                context['mess'] = 'Registration Successful'
                return redirect('bankbranches')

    return HttpResponse(template.render(context,request))

def bank_branches(request):
    template = loader.get_template('bank/bank_sub_branches.html')
    context = {'mess': ''}
    context['user_mail'] = user_mail = request.session['mail']
    context['uobj'] = uobj = Users.objects.get(user_mail=user_mail)
    context['urobj'] = urobj = Users.objects.all()
    context['bbobj'] = bbobj = Blood_bank.objects.filter(user_main_branch_name=uobj.user_main_branch_name).order_by('bank_name')
    context['uuobj'] = uuobj = Users.objects.filter(user_main_branch_name=uobj.user_main_branch_name).order_by('user_name')

    if uobj.user_main_branch_name == uobj.user_name:
      context['main'] = 'yes'

    return HttpResponse(template.render(context, request))

# ------------------- Hospital

def hos_display_blood(request):
    template = loader.get_template('hospital/hos_display_blood.html')
    context = {'mess': ''}
    context['ureg'] = ureg = Users.objects.order_by('user_name')
    context['user_mail'] = user_mail = request.session['mail']
    context['uobj'] = uobj = Users.objects.get(user_mail=user_mail)
    context['bval'] = bval = Blood_bank.objects.order_by('bank_name')

    return HttpResponse(template.render(context, request))

def hos_noti(request):
    template = loader.get_template('hospital/hos_noti.html')
    context = {'mess': ''}
    context['ureg'] = ureg = Users.objects.all()
    context['user_mail'] = user_mail = request.session['mail']
    context['ureg'] = ureg = Users.objects.get(user_mail=user_mail)

    context['bobj'] = bobj = Donor_reports.objects.all()
    context['bsobj'] = bsobj = Blood_seek.objects.all()

    return HttpResponse(template.render(context, request))

def hos_seek(request):
    template = loader.get_template('hospital/hos_seek.html')
    context = {'mess': ''}

    context['bvobj'] = bvobj = Blood_bank.objects.order_by('bank_name')
    context['user_mail'] = user_mail = request.session['mail']
    context['ureg'] = ureg = Users.objects.get(user_mail=user_mail)

    mail = request.session['mail']
    role = request.session['type']

    if request.method == 'POST':
        units = request.POST.get('units')
        group = request.POST.get('group')
        bankname = request.POST.get('bankname')

        bsobj = Blood_seek.objects.create(
            bank_name=bankname,
            group=group,
            mail=mail,
            units=units,
            role=role
        )

        bsobj.save()

        context['mess'] = 'request forwarded to Blood Bank'

    return HttpResponse(template.render(context, request))

def hos_don_report(request):
    template = loader.get_template('hospital/hos_don_report.html')
    context = {'mess': ''}
    context['ureg'] = ureg = Users.objects.all()
    rg = 0
    context['user_mail'] = user_mail = request.session['mail']
    uobj = Users.objects.get(user_mail=user_mail)

    context['bvobj'] = bvobj = Blood_bank.objects.order_by('user_name')
    context['bobj'] = bobj = Donor_reports.objects.all()

    if request.method == 'POST':

        group = str(request.POST.get('group'))
        location = str(request.POST.get('location')).title()

        for x in bobj:
            rg = 1

            if x.user_location == location and str(x.group) == str(group):
                print(x.user_location, location, group, x.group, x.status, x.bol)
                context['mess'] = 'yes'
                context['bg'] = str(x.group)
                context['bl'] = str(x.user_location)

        if context['mess'] == '' and rg == 1:
            context['rep'] = 'No Results found, please search again'

    return HttpResponse(template.render(context, request))

# ------------------------ Seek

def blood_avai(request):
    template = loader.get_template('seek/blood_avai.html')
    context = {'mess': ''}
    context['ureg'] = ureg = Users.objects.order_by('user_name')
    context['user_mail'] = user_mail = request.session['mail']
    context['uobj'] = uobj = Users.objects.get(user_mail=user_mail)
    context['bval'] = bval = Blood_bank.objects.order_by('bank_name')


    return HttpResponse(template.render(context,request))

def seek_blood(request):
    template = loader.get_template('seek/seek_blood.html')
    context = {'mess': ''}

    context['bvobj'] = bvobj = Blood_bank.objects.order_by('bank_name')
    context['user_mail'] = user_mail = request.session['mail']
    context['ureg'] = ureg = Users.objects.get(user_mail=user_mail)

    mail = request.session['mail']
    role = request.session['type']

    if request.method == 'POST':
        units = request.POST.get('units')
        group = request.POST.get('group')
        bankname = request.POST.get('bankname')

        bsobj = Blood_seek.objects.create(
            bank_name=bankname,
            group=group,
            mail=mail,
            units=units,
            role=role
        )

        bsobj.save()

        context['mess'] = 'request forwarded to Blood Bank'

    return HttpResponse(template.render(context,request))

# --------------------------- Donor

def donor_home(request):
    template = loader.get_template('donor/donor_home.html')
    context = {'mess': ''}
    context['user_mail'] = user_mail = request.session['mail']
    ureg = Users.objects.get(user_mail=user_mail)
    context['name'] = ureg.user_name
    context['bval'] = bval = Blood_bank.objects.order_by('bank_name')
    c = 0
    if request.method == 'POST':
        for x in Donor_reports.objects.all():
            if x.mail == user_mail:
                x.bol = 'old'
                x.save()

        mail = user_mail
        age = request.POST.get('age')
        bankname = request.POST.get('bankname')
        bp = request.POST.get('bp')
        diease = request.POST.get('ddis')
        diabetes = request.POST.get('diabetes')
        units = request.POST.get('units')
        group = request.POST.get('group')
        physical_disorders = request.POST.get('physical_disorders')
        date = request.POST.get('ddate')
        user_location = ureg.user_address
        bol = 'latest'

        pdate = (datetime.now()).date()
        format_str = '%Y-%m-%d'
        cd = datetime.strptime(date, format_str)
        cd_day = cd.day
        cd_month = cd.month
        cd_year = cd.year
        date = cd.date()
        print(cd.date())
        if cd_year >= pdate.year:
            if cd_month == pdate.month:
                if cd_day >= pdate.day:
                    context['mess'] = ''
                else:
                    context['mess'] = 'Enter proper Date'
            elif cd_month > pdate.month:
                if cd_day <= pdate.day:
                    context['mess'] = ''
                else:
                    context['mess'] = 'Enter proper Date'
            else:
                context['mess'] = 'Enter proper Date'
        else:
            context['mess'] = 'Enter proper Date'

        if context['mess'] == '':

            btest = Donor_reports.objects.all()
            for x in btest:
                if x.mail == mail and x.bank_name == bankname and x.status == 'not yet approved':
                    c = 1
                    x.age = age
                    x.location = user_location
                    x.bp = bp
                    x.diease = diease
                    x.diabetes = diabetes
                    x.units = units
                    x.group = group
                    x.physical_disorders = physical_disorders
                    x.date = date
                    x.user_location = user_location
                    x.bol = bol
                    x.save()
                    context['mess'] = 'Donor Registration successful and Request sent to Blood Bank'

            if c == 0:
                bobj = Donor_reports.objects.create(
                    mail=mail,
                    age=age,
                    bank_name=bankname,
                    bp=bp,
                    diease=diease,
                    diabetes=diabetes,
                    units=units,
                    group=group,
                    physical_disorders=physical_disorders,
                    date=date,
                    user_location=user_location,
                    bol=bol
                )
                bobj.save()
                context['mess'] = 'Donor Registration successful and Request sent to Blood Bank'

    return HttpResponse(template.render(context, request))

def donor_profile(request):
    template = loader.get_template('donor/donor_profile.html')
    context = {'mess': ''}
    context['user_mail'] = user_mail = request.session['mail']
    context['ureg'] = ureg = Users.objects.get(user_mail=user_mail)

    context['user_name'] = ureg.user_name
    context['user_mail'] = ureg.user_mail
    context['user_pass'] = ureg.user_pass
    context['user_phone_number'] = ureg.user_phone_number
    context['user_address'] = ureg.user_address

    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_pass = request.POST.get('user_pass')
        user_phone_number = request.POST.get('user_phone_number')
        user_address = request.POST.get('user_address')

        try:
            user_phone_number == int(user_phone_number)
        except:
            context['mess'] += ' Enter Phone number correctly '

        if context['mess'] == '':
            ureg.user_name = user_name
            ureg.user_pass = user_pass
            ureg.user_phone_number = user_phone_number
            ureg.user_address = user_address

            ureg.save()
            context['mess'] = 'Profile Data Updated'
    return HttpResponse(template.render(context,request))

def donor_notification(request):
    template = loader.get_template('donor/donor_notification.html')
    context = {'mess': ''}

    context['ureg'] = ureg = Users.objects.all()
    context['user_mail'] = user_mail = request.session['mail']
    context['ureg'] = ureg = Users.objects.get(user_mail=user_mail)
    context['bobj'] = bobj = Donor_reports.objects.all()
    context['bsobj'] = bsobj = Blood_seek.objects.all()

    for x in bsobj:
        print(x.status)

    return HttpResponse(template.render(context, request))
