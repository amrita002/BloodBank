from django.db import models

class Users(models.Model):

    user_name = models.CharField(max_length=20)
    user_main_branch_name = models.CharField(max_length=20,default='main')
    user_mail = models.EmailField()
    user_pass = models.CharField(max_length=20)
    user_role = models.CharField(max_length=10)
    user_phone_number = models.CharField(max_length=10,default='0000000000')
    user_address = models.TextField()

    def __str__(self):
        return self.user_name

    class Meta:
        verbose_name_plural = 'Users'

class Blood_bank(models.Model):

    mail = models.EmailField()
    location = models.CharField(max_length=30, default='')
    user_main_branch_name = models.CharField(max_length=20, default='main')
    bank_name = models.CharField(max_length=30, default='')
    a_positive = models.IntegerField(default=0)
    b_positive = models.IntegerField(default=0)
    ab_positive = models.IntegerField(default=0)
    o_positive = models.IntegerField(default=0)
    a_negative = models.IntegerField(default=0)
    b_negative = models.IntegerField(default=0)
    ab_negative = models.IntegerField(default=0)
    o_negative = models.IntegerField(default=0)

    def __str__(self):
        return self.mail

    class Meta:
        verbose_name_plural = 'Blood_bank'

class Donor_reports(models.Model):

    bank_name = models.CharField(max_length=30, default='')
    location = models.CharField(max_length=30, default='')
    user_location = models.CharField(max_length=30,null=True,blank=True)
    mail = models.EmailField()
    age = models.IntegerField()
    group = models.CharField(max_length=20)
    bp = models.CharField(max_length=6, default=None)
    diabetes = models.CharField(max_length=3,default='no')
    physical_disorders = models.CharField(max_length=3,default='no')
    diease = models.CharField(max_length=20,default='no')
    status = models.CharField(max_length=50,default='not yet approved')
    units = models.IntegerField(default=0)
    date = models.DateField(null=True,blank=True)
    bol = models.CharField(default='latest',max_length=10)

    def __str__(self):
        return self.mail

    class Meta:
        verbose_name_plural = 'Donor_reports'

class Blood_seek(models.Model):

    bank_name = models.CharField(max_length=30, default='')
    mail = models.EmailField()
    group = models.CharField(max_length=10,default='')
    units = models.IntegerField()
    location = models.CharField(max_length=20, default='')
    status = models.CharField(max_length=50, default='not yet approved')
    role = models.CharField(max_length=10,default='')

    def __str__(self):
        return self.mail

    class Meta:
        verbose_name_plural = 'Blood_seek'
