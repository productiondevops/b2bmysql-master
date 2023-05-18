from core.UtilityView import *
from .views import *
from django.urls import path,re_path
from .booking import *
 
from django.contrib.auth.views import LogoutView
urlpatterns = [
path('',dashboard,name='home'),
path('home/',dashboard,name='dashboard'),
path('dashboard/',dashboard,name='dashboard'),
path('success/',success,name='success'),
path('clientreport/',clientreport,name="clientreport"),
path('invoice/',invoice,name="invoice"),
path('tracking/', tracking, name='tracking'),
#path('TrackShipment/<waybillno1>', tracking1, name='tracking-waybill'),

path('SuccessView/',SuccessView,name="SuccessView"),
path('add-to-favourite/',add_to_favourite,name="add-to-favourite"),
path('favouritebooking/',favouritebooking,name="favouritebooking"),
 
path('reschedulebooking/<int:id>',reschedulebooking,name="reschedulebooking"),
  
#path('printbooking/',PrintBooking,name="printbooking"), 
path('deletebooking/<int:id>',deletebooking,name="deletebooking"),
path('deleteUploadBooking/<int:id>',deleteUploadBooking,name="deleteUploadBooking"),
path('newconsignee/',newconsignee,name="newconsignee"),
path('Registeration/',Register,name="Register"),
path('Enquiries/',Enquiries,name="Enquiries"),
path('edd/', estimated_delivery, name='edd'),
path('profile/', basecompanyprofile, name='profile'),

path('get/ajax/validate/cities', checkCities, name="validate_checkCities"),
path('post/ajax/data/saveEDD', saveEDD, name="save_edd"),
path('getconsignee/<str:consigneeid>/', getconsignee, name='getconsignee'),

path('logoff/', LogoutView.as_view(next_page='/'), name='logoff'), 
path('premium-login/', b2blogin, name='b2blogin'),
#re_path(r"^(?:page-(?P<page_number>\d+)/)?$", booking, name="bookinglistview"),
#path('booking/', bookingHTMxTableView.as_view(),name='booking'),
path('create-pdf', pdf_report_create, name="create-pdf"),
path('alertnotification/<int:booking_id>/<int:alert_type>', alertnotification, name="alertnotification"), 

path('UploadBooking', UploadBooking, name="UploadBooking"),
#path('reset_password', reset_password, name="reset_password"),
path("password_reset/", password_reset_request, name="password_reset"),
path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='b2bportal/password/password_reset_done.html'), name='password_reset_done'),
path('reset/<uidb64>/<token>/', B2BPasswordResetConfirmView.as_view(template_name="b2bportal/password/password_reset_confirm.html"), name='password_reset_confirm'),
path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='b2bportal/password/password_reset_complete.html'), name='password_reset_complete'),  
path('printbooking/',PrintBooking,name="printbooking"), 

#autocomplete
path('country-autocomplete/',
        CountryAutocomplete.as_view(),
        name='country-autocomplete',
    ),

path('city-autocomplete/',
        CityAutocomplete.as_view(),
        name='city-autocomplete',
    ),

# new Urls
path('confirm-booking/<int:booking_id>/',ConfirmBooking,name="confirm-booking"),
path('booking/<int:booking_id>/',newbooking,name="booking"),
path('booking-view/',BookingView,name="booking-view"),
path('booking-list/',booking_list,name="booking-list"),
path('shipper-lookup/', shipper_lookup, name='shipper-lookup'),
path('reciver-address-lookup/', reciver_address_lookup, name='reciver-address-lookup'),
path('dimensions/', dimensions, name='dimensions'),
path('add-new-shipper/', add_new_shipper, name='add-new-shipper'),
path('getembedinfo', get_embed_info,name="/getembedinfo"),
path('Price_Estimator/', Price_Estimator, name='Price_Estimator'),
# path('LoadType/', LoadType, name='LoadType'),
]  

