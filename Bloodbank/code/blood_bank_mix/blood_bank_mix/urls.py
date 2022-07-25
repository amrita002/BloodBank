from django.contrib import admin
from django.urls import path
from blood import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('reg/', views.reg, name='reg'),
    path('regack/', views.reg_ack, name='reg_ack'),
    path('logout/', views.logout, name='logout'),
    path('forgot/', views.forgot, name='forgot'),
    path('sam/', views.sam, name='sam'),

    # ------------------ Blood Bank ----------------

    path('bankhome/', views.bank_home, name='bankhome'),
    path('bankdonreq/', views.bank_don_req, name='bankdonreq'),
    path('bankseekreq/', views.bank_seek_req, name='bankseekreq'),
    path('bankhosreq/', views.bank_hos_req, name='bankhosreq'),
    path('bankdonreport/', views.bank_don_report, name='bankdonreport'),
    path('bankbranches/', views.bank_branches, name='bankbranches'),
    path('bankaddbranches/', views.bank_add_branch, name='bankaddbranches'),

    # ------------------- Hospital -------------------

    path('hosnoti/', views.hos_noti, name='hosnoti'),
    path('hosdisplayblood',views.hos_display_blood,name='hosdisplayblood'),
    path('hosseek/',views.hos_seek,name='hosseek'),
    path('hosdonreport',views.hos_don_report,name='hosdonreport'),

    # ------------------- Seek -------------------

    path('bloodavai/',views.blood_avai,name='bloodavai'),
    path('seekblood',views.seek_blood,name='seekblood'),

    # ------------------- Donor -------------------

    path('donorhome/',views.donor_home,name='donorhome'),
    path('donorprofile/',views.donor_profile,name='donorprofile'),
    path('donornoti/',views.donor_notification,name='donornoti'),

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_ROOT, document_root=settings.MEDIA_ROOT)