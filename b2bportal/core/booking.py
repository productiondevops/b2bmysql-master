from django.http import HttpResponse
from .UtilityView import *
from time import strftime
from django.db import models
from .models import CompanyProfile,StandardCode,country,city,consignee,shipmenttype,shipper
from django import forms
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.forms import IntegerField
from dal import autocomplete
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django_tables2 import SingleTableMixin, TemplateColumn
import django_tables2 as tables
from django_filters.views import FilterView
import django_filters
from django_filters.views import FilterView
from sequences import Sequence
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages #import messages
WaybillNumber = Sequence("waybill_numbers",initial_value=242349445)
document_no = Sequence("doc_numbers",initial_value=1000)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tablib import Dataset
import requests
## Models

PAYMENT_METHOD = [
    ('Cash', 'Cash'),
    ('Account', 'Shipper-Account'),
    ('COD', 'Cash-On-Delivery'),  
]

BOOKING_STATUS = [
    ('Booked', 'Booked'),
    ('Courier-Informed', 'Courier-Informed'),
    ('Cancel-Booking', 'Cancel-Booking'),
    ('Scheduled', 'Scheduled'),
    ('Picked-Up','Picked-Up'),
    ('Miss-PickUp','Miss-PickUp'),
    ('Acknowledge','Acknowledge'),   
]

class Booking(models.Model):
    bookingref = models.CharField( max_length=8, blank=True, null=True, verbose_name=_(u'Booking#'))
    waybillno = models.CharField(verbose_name=u"Waybill No",max_length=100, null=True, blank=True)
    reference = models.CharField(max_length=100, null=True, blank=True)
    company_profile = models.ForeignKey("CompanyProfile",related_name="booking_comapny_name", on_delete=models.SET_NULL,null=True, blank=True)
    shipper=models.ForeignKey("shipper",related_name="shipper_booking", on_delete=models.SET_NULL,null=True, blank=True)
    consignee=models.ForeignKey("consignee",related_name="consignee_booking", on_delete=models.SET_NULL,null=True, blank=True)
    shipment_type=models.ForeignKey("shipmenttype",related_name="booking_shipment_type", on_delete=models.SET_NULL,null=True, blank=True)
    gross_weight=models.FloatField(default=0.0,null=True, blank=True)
    piece_count=models.IntegerField(default=1, null=True,blank=True)
    chargable_weight=models.FloatField(default=0.0,null=True, blank=True)
    customs_value=models.FloatField(default=0.0,null=True, blank=True)
    goods_origin=models.CharField(max_length=100, null=True, blank=True)
    remarks=models.CharField(max_length=100, null=True, blank=True)
    goods_description=models.CharField(max_length=100, null=True, blank=True)
    additonal_services=models.CharField(max_length=100, null=True, blank=True)
    booking_date=models.DateField(default=datetime.date.today, null=True, blank=True)      
    ready_time=   models.TimeField(null=True, blank=True)          
    Latest_time= models.TimeField(null=True, blank=True)
    payment_method=models.CharField(verbose_name=u"Payment method",
                                  max_length=50,
                                  choices=PAYMENT_METHOD,
                                  default='Cash', null=True, blank=True)

  
   
    
    pickup_date = models.DateField(verbose_name="Pickup Date",null=True, blank=True)
    pickup_time = models.TimeField(verbose_name="Pickup Time",null=True, blank=True)
    
    booking_status= models.CharField(verbose_name=u"Booking Status",
                                  max_length=25,
                                  choices=BOOKING_STATUS,
                                  default='Booked', null=True, blank=True)
    
    request_for_schedule_pickup=models.BooleanField(default=False,null=True,blank=True)
    save_to_addressbook=models.BooleanField(default=False,null=True,blank=True)
    is_confirmed =models.BooleanField(default=False,null=True, blank=True)
    is_SMS = models.BooleanField(default=False,null=True, blank=True)
    is_Push = models.BooleanField(default=False,null=True, blank=True)    
    is_Email =models.BooleanField(default=False,null=True, blank=True)
    is_fav =models.BooleanField(default=False,null=True, blank=True)
    insurance_value=models.FloatField(default=0.0,null=True, blank=True)
    declare_value=models.FloatField(default=0.0,null=True, blank=True)
    created_date_time=models.DateTimeField(default=now, null=True, blank=True)
    status_id=models.IntegerField(default=1, null=True,blank=1) 

    def save(self, *args, **kwargs):
        if self.__class__.objects.all().count() == 0:
            letter =  "BK"
            number = 1
            self.bookingref ="{0}{1:0>2d}".format(letter,number)   # 'A001' this time
        else:
            last_id = self.__class__.objects.all().order_by("-id")[0].id + 1
            letter =  "BK"
            number = (last_id+1)
            self.bookingref = "{0}{1:0>2d}".format(letter,number)
        super(self.__class__, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.company_profile} "


class CustomerWaybill(models.Model):
    reference = models.CharField(max_length=100, null=True, blank=True)
    booking_no = models.ForeignKey("Booking",related_name="customer_booking_no", on_delete=models.SET_NULL,null=True, blank=True)
    company_profile = models.ForeignKey("CompanyProfile",related_name="customer_comapny_name", on_delete=models.SET_NULL,null=True, blank=True)
    shipper=models.ForeignKey("shipper",related_name="customer_shipper_booking", on_delete=models.SET_NULL,null=True, blank=True)
    consignee=models.ForeignKey("consignee",related_name="customer_consignee_booking", on_delete=models.SET_NULL,null=True, blank=True)
    shipment_type=models.ForeignKey("shipmenttype",related_name="customer_shipment_type", on_delete=models.SET_NULL,null=True, blank=True)
    gross_weight=models.FloatField(default=0.0,null=True, blank=True)
    piece_count=models.IntegerField(default=1, blank=True)
    chargable_weight=models.FloatField(default=0.0,null=True, blank=True)
    customs_value=models.FloatField(default=0.0,null=True, blank=True)
    goods_origin=models.CharField(max_length=100, null=True, blank=True)
    remarks=models.CharField(max_length=100, null=True, blank=True)
    goods_description=models.CharField(max_length=100, null=True, blank=True)
    additonal_services=models.CharField(max_length=100, null=True, blank=True)
    booking_date=models.DateField(default=datetime.date.today, null=True, blank=True)      
    ready_time=   models.TimeField(null=True, blank=True)          
    Latest_time= models.TimeField(null=True, blank=True)
    payment_method=models.CharField(verbose_name=u"Payment method",
                                  max_length=50,
                                  choices=PAYMENT_METHOD,
                                  default='Cash', null=True, blank=True)

    
    bookingref = models.CharField( max_length=8, blank=True, null=True, verbose_name=_(u'Booking#'))
    
    pickup_date = models.DateField(verbose_name="Pickup Date",null=True, blank=True)
    pickup_time = models.TimeField(verbose_name="Pickup Time",null=True, blank=True)
    
    booking_status= models.CharField(verbose_name=u"Booking Status",
                                  max_length=25,
                                  choices=BOOKING_STATUS,
                                  default='Booked', null=True, blank=True)
    save_to_addressbook=models.BooleanField(default=False,null=True,blank=True)
    request_for_schedule_pickup=models.BooleanField(default=False,null=True,blank=True)
    is_SMS = models.BooleanField(default=False,null=True, blank=True)
    is_Push = models.BooleanField(default=False,null=True, blank=True)    
    is_Email =models.BooleanField(default=False,null=True, blank=True)
    is_fav =models.BooleanField(default=False,null=True, blank=True)
        
    def save(self, *args, **kwargs):
        if self.__class__.objects.all().count() == 0:
            letter =  "BK"
            number = 1
            self.bookingref ="{0}{1:0>2d}".format(letter,number)   # 'A001' this time
        else:
            last_id = self.__class__.objects.all().order_by("-id")[0].id + 1
            letter =  "BK"
            number = (last_id+1)
            self.bookingref = "{0}{1:0>2d}".format(letter,number)
        super(self.__class__, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.company_profile} "


class Dimensions(models.Model): 
    booking_no = models.ForeignKey("Booking",related_name="Dimensions_booking_no", on_delete=models.SET_NULL,null=True, blank=True)
    pieces=models.IntegerField(default=1, blank=True)
    weight=models.FloatField(default=0.0,null=True, blank=True)
    vol_weight=models.FloatField(default=0.0,null=True, blank=True)
    gross_weight=models.FloatField(default=0.0,null=True, blank=True)
    chargable_weight=models.FloatField(default=0.0,null=True, blank=True)
    length=models.FloatField(default=0.0,null=True, blank=True)
    width=models.FloatField(default=0.0,null=True, blank=True)
    height=models.FloatField(default=0.0,null=True, blank=True)
    know_my_dimension=models.BooleanField(default=False,null=True,blank=True)  
    current_session=models.CharField( max_length=200, blank=True, null=True, verbose_name=_(u'Current_Session#'))





## Models

# FORMS 
class SelectedReceiverForm(forms.ModelForm):
    company_name = forms.CharField(
        required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }))
    address = forms.CharField(
        required=False, max_length=100, widget=forms.Textarea(attrs={'class': 'form-control form-control-sm', }))

    contact_department =forms.CharField(
        required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }))
    
    country =forms.ModelChoiceField(required=False,queryset=country.objects.all(),widget=forms.Select({'class': 'form-control form-control-sm', }))
    mobile = forms.CharField(
        required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }))
    
    city = forms.ModelChoiceField(required=False,queryset=city.objects.all(),widget=forms.Select({'class': 'form-control form-control-sm', }))
    fax=forms.CharField(
        required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }))
    state=forms.CharField(
        required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }))
    reference = forms.CharField(
        required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }))
    postal_code = forms.CharField(
        required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }))
    save_to_addressbook=  forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control form-control-sm', }))    

    class Meta:
        model = Booking
        fields=('company_name','address','contact_department','country','mobile','city','fax','state','reference','postal_code',  'save_to_addressbook' )    
 

class ShipmentBookingForm(forms.ModelForm):
    # country=forms.ModelChoiceField(required=True, queryset=country.objects.all(),
    #                                     widget=autocomplete.ModelSelect2(url='/country-autocomplete/',
    #                                     attrs={'style':'width:250px!important;'}
    #                                    ))


    # city=forms.ModelChoiceField(required=True, queryset=city.objects.all(),
    #                                     widget=autocomplete.ModelSelect2(url='/city-autocomplete/',
    #                                     forward=('country',),
    #                                     attrs={'style':'width:250px!important;'}
    #                                    ))      


         
    def __init__(self, *args, **kwargs):
        super(ShipmentBookingForm, self).__init__(*args, **kwargs)
        self.fields['pickup_date'].initial = datetime.date.today
        self.fields['ready_time'].initial = datetime.time
        self.fields['Latest_time'].initial = datetime.time
        # session=None
        # session['clientID'] = "9020211"
       
        # if session['clientID'] is not None:
        #     self.fields['shipment_type'].queryset = shipmenttype.objects.filter(id=1)


    shipper=forms.CharField(required=False,widget=forms.HiddenInput())
    company_name = forms.CharField(
        required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }))
    address = forms.CharField(
        required=True, max_length=100, widget=forms.Textarea(attrs={'class': 'form-control form-control-sm', }))

    contact_department =forms.CharField(
        required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }))
    
    country =forms.ModelChoiceField(required=False,queryset=country.objects.all(),widget=forms.Select({'class': 'form-control form-control-sm', }))
    mobile = forms.CharField(
        required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }))
    
    city = forms.ModelChoiceField(required=False,queryset=city.objects.all(),widget=forms.Select({'class': 'form-control form-control-sm', }))
    fax=forms.CharField(
        required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }))
    state=forms.CharField(
        required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }))
    reference = forms.CharField(
        required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }))
    postal_code = forms.CharField(
        required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }))
    shipment_type =forms.ModelChoiceField(required=False,queryset=shipmenttype.objects.all(),widget=forms.Select({'class': 'form-control form-control-sm', }))
    gross_weight = forms.DecimalField()
    additonal_services =forms.CharField(
        required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }))
    chargable_weight = forms.DecimalField()

    goods_origin = forms.CharField(
        required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }))

    piece_count = forms.CharField(
        required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }))

    customs_value = forms.DecimalField(
        required=False,  widget=forms.NumberInput (attrs={'class': 'form-control form-control-sm' }))
    
    remarks = forms.CharField(
        required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm','placeholder':_('National ID') }))
    
    goods_description = forms.CharField(
        required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    pickup_date= forms.DateField(required=False,  widget=forms.DateInput(
        attrs={
            'type': 'date',
            'class': 'form-control',
            'min': datetime.date,
        }
    ))             

                
    
    ready_time  = forms.TimeField(required=False, initial=strftime("%I:%M %p"),  widget=forms.TimeInput(
        attrs={
            'type': 'time',
            'class': 'form-control',

        }
    ))
    Latest_time  = forms.TimeField(required=False, initial=strftime("%I:%M %p"),  widget=forms.TimeInput(
        attrs={
            'type': 'time',
            'class': 'form-control',

        }
    ))
    CHOICES = [
    ('Cash', 'Cash'),
    ('Shipper-Account', 'Shipper-Account'),  
    ]
    
    payment_method = forms.ChoiceField(required=False,choices=CHOICES, widget=forms.RadioSelect)
    request_for_schedule_pickup=  forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control form-control-sm', }))
    save_to_addressbook=  forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control form-control-sm', }))   
    insurance_value = forms.DecimalField(
        required=False,  widget=forms.NumberInput (attrs={'class': 'form-control form-control-sm','placeholder':_('Insurance Value') }))
    declare_value = forms.DecimalField(
        required=False,  widget=forms.NumberInput (attrs={'class': 'form-control form-control-sm','placeholder':_('Declare Value') }))      
    
    class Meta:
        model = Booking
        fields=('company_name','address','contact_department','country','mobile','city','fax','state','reference','postal_code','shipment_type','gross_weight','additonal_services','chargable_weight','goods_origin','piece_count','customs_value','remarks','goods_description','ready_time','Latest_time','payment_method','request_for_schedule_pickup','save_to_addressbook','waybillno','insurance_value','declare_value')    
 
class AddNewShipperForm(forms.ModelForm):
    # country=forms.ModelChoiceField(required=True, queryset=country.objects.all(),
    #                                     widget=autocomplete.ModelSelect2(url='/country-autocomplete/',
    #                                     attrs={'style':'width:250px!important;'}
    #                                    ))


    # city=forms.ModelChoiceField(required=True, queryset=city.objects.all(),
    #                                     widget=autocomplete.ModelSelect2(url='/city-autocomplete/',
    #                                     forward=('country',),
    #                                     attrs={'style':'width:250px!important;'}
    #                                    ))      

    company_name = forms.CharField(
        required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control no-border form-control-sm'}))
    
    contact_person = forms.CharField(
        required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control no-border form-control-sm'}))
    contact_number = forms.CharField(
        required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm' }))

    mobile_number =forms.CharField(
        required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm' }))

    address=forms.CharField(
        required=False, max_length=100, widget=forms.Textarea(attrs={'class': 'form-control form-control-sm','row':4,'cols':100 }))
    country=forms.ModelChoiceField(required=True,queryset=country.objects.all(),widget=forms.Select({'class': 'form-control form-control-sm', }))
    city=forms.ModelChoiceField(required=True,queryset=city.objects.all(),widget=forms.Select({'class': 'form-control form-control-sm', }))
    pickup_point=forms.CharField(
        required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }))
    shipping_instruction=forms.CharField(
        required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', }))
     
    class Meta:
        model = shipper
        fields=('company_name','contact_person','contact_number','mobile_number','address','country','city','pickup_point','shipping_instruction','account_number')    

class DimensionsForm(forms.ModelForm):
    pieces = forms.CharField(
        required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-sm','placeholder':_('Pieces') }))
    weight=forms.DecimalField(required=False)
    vol_weight=forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Vol.Wt'}))
    gross_weight= forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Gross Weight'}))
    chargable_weight= forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Chargable Weight'}))
    length= forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Length'}))
    width=forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Width'}))
    height=forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Height'}))
    know_my_dimension=forms.BooleanField(
        required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control form-control-sm', }))

    class Meta:
        model = Dimensions
        fields=('pieces','weight','vol_weight','gross_weight','chargable_weight','length','width','height','know_my_dimension')    
class reschedulebookingForm (forms.ModelForm):

    PickUp= forms.DateField(label="pickup_date",
                                  widget=forms.DateInput(attrs={'placeholder': _('Pick A Date'), 'type': 'date','class': 'form-control placeholdercolor'}))
    PickupTime= forms.TimeField(label="close_time",

                                  widget=forms.TimeInput(attrs={'placeholder': _('Pick A time'), 'type': 'time','class': 'form-control placeholdercolor'}))
    OfficeUpto =forms.TimeField(label="close_time",

                                  widget=forms.TimeInput(attrs={'placeholder': _('Pick A time'), 'type': 'time','class': 'form-control placeholdercolor'}))
    SchedulingReason=forms.ModelChoiceField(queryset=SchedulingReason.objects.all(),widget= forms.Select({'class': 'form-control','placeholder':_('Reason') }))

    class Meta:
        model = Booking
        fields=('pickup_date', 'pickup_time', 'OfficeUpto','SchedulingReason')
class B2BLoginForm(forms.Form):
    username = forms.CharField(
         widget=forms.TextInput({'class': 'form-control', }))
    password = forms.CharField(
        widget=forms.PasswordInput({'class': 'form-control', }))

class ClientForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['from_date'].initial = date.today
        self.fields['to_date'].initial = date.today

    clientid = forms.CharField(label=_("Client ID"), max_length=300, help_text='Required',
                               widget=forms.Textarea({
                                   'class': 'form-control form-control-sm',
                                   'rows': 5,
                                   'width': '100%',
                                   }))
    from_date= forms.DateField(label="From Date",
                                  widget=forms.DateInput(attrs={'placeholder': _('From Date'), 'type': 'date','class': 'form-control placeholdercolor'}))
    to_date= forms.DateField(label="To Date",
                                  widget=forms.DateInput(attrs={'placeholder': _('To Date'), 'type': 'date','class': 'form-control placeholdercolor'}))   

# FORMS

#Views 

def ConfirmBooking(request,booking_id):
    waybill_list=Booking.objects.filter(pk=booking_id)
    print('waybill_list',waybill_list)
    if waybill_list.count() > 0:
        company=GetCurrentCompany(request)
        booking=waybill_list[0]
        booking.is_confirmed=True
        booking.waybillno=next(WaybillNumber)
        booking.save()

        return render(request, 'b2bportal/confirm.html', {
                'booking': booking,
                'waybills': waybill_list,
                'company': company,
            })
    else:
        return HttpResponse(status=204)


def GetCurrentCompany(request):
    company=None
    for comp in CompanyProfile.objects.all():
        data = comp.allowed_users.all().filter(id=request.user.id)
        if data:
            company = comp
            break
    return company
 

class BookingFilter(django_filters.FilterSet):
    
    start_date = django_filters.DateFilter(field_name='pickup_date',
                                           widget= forms.DateInput(attrs={'class': 'form-control dateheight', 'type': 'date','value':"2023-05-02"}  ),
                                         label='',method='universal_search')
                                        
    end_date = django_filters.DateFilter(field_name='pickup_date',
                                         widget= forms.DateInput(attrs={'class': 'form-control dateheight', 'type': 'date','value':"2023-05-02"}),
                                          label='',method='universal_search')

    query = django_filters.CharFilter(method='universal_search1', label="", widget=forms.TextInput(attrs={'class': 'form-control ml-5 dateheight','placeholder': 'Filter(waybill,org,dest,status,Type)',}))
    #query = django_filters.CharFilter(field_name='booking_no__booking_status', label="", widget=forms.TextInput(attrs={'class': 'form-control ml-5','placeholder': 'Filter(waybill,org,dest,status,Type)',}))

    
    def __init__(self, *args, **kwargs):
        super(BookingFilter, self).__init__(*args, **kwargs)
        self.form.initial['start_date'] = datetime.date.today()
        self.form.initial['end_date'] = datetime.date.today()
        print(datetime.date.today())

    


    class Meta:
        model = Booking
        fields = ['start_date','end_date']

    def universal_search(self, queryset, booking_no, value):
        # print("AAA",self.data.get("start_date",None))
        start_date=self.data.get("start_date",None)
        end_date=self.data.get("end_date",None)
        query=self.data.get("query",None)
        if query is None:
            print('query none')
            query="pickup"
         
       
        #qs= CustomerWaybill.objects.filter(booking_no__pickup_date__gte=start_date,booking_no__pickup_date__lte =end_date,booking_no__booking_status=query).order_by("-booking_no__pickup_date")
        #print(qs)
        qs= Booking.objects.filter(pickup_date__gte=start_date,pickup_date__lte =end_date)
        
        return qs
    def universal_search1(self, queryset, booking_no, value):
        print('query none')
        start_date=self.data.get("start_date",None)
        end_date=self.data.get("end_date",None)
        query=self.data.get("query",None)
        if query is None:
            print('query none')
            query="pickup"
        print(start_date,end_date,query)
       
        #qs= Booking.objects.filter(pickup_date__gte=start_date,pickup_date__lte =end_date,status_id=1,booking_status=query).order_by("-pickup_date")
        #print(qs)
        return Booking.objects.filter(Q(waybillno=value) | Q(bookingref=value) )
        
        return qs

    # def get_queryset(self):
    #     start_date=self.request.GET.get("start_date",None)
    #     end_date=self.request.GET.get("end_date",None)
    #     qs= CustomerWaybill.objects.filter(booking_no__pickup_date__gte=start_date,booking_no__pickup_date__lte =end_date).order_by("-pickup_date")
    #     print('Rashmi queryset1')
    #     return super().get_queryset()


class BookingHTMxTable(tables.Table):

    action = TemplateColumn(template_code="""
    
    {% if record.booking_no.booking_status == "Cancel-Booking" %} &nbsp;
    {% else %}
    <ul class="navbar-nav">
                <li class="nav-item  dropdown">
                <a class="nav-link dropdown-toggle" href="http://example.com" id="navbarDropdownMenuLink" data-toggle="dropdown">
               
                </a>
                <div class="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdownMenuLink">
                    
                  <a class="dropdown-item" style="color: blue;{% if record.booking_no.booking_status == "Picked-Up" %} display:None;{%endif%}"  href="{% url 'home:newbooking' record.booking_no.pk record.pk %}"><i class="fa fa-edit fa-2x mr-2 bg-blue"></i> Edit</a>
                  <a class="dropdown-item" style="color: red;{% if record.booking_no.booking_status == "Picked-Up" %} display:None;{%endif%}"   hx-get="{% url 'home:deletebooking' record.booking_no.pk %}" hx-confirm="Are you sure you want to delete this customer?" hx-target="#dialog" href="{% url 'home:deletebooking' record.booking_no.pk %}" ><i class="fa fa-trash fa-2x mr-2"></i> Delete</a>
                  <a class="dropdown-item" style="color: blue;{% if record.booking_no.booking_status == "Picked-Up" %} display:None;{%endif%}"  hx-get="/reschedulebooking/{{record.booking_no.pk}}" hx-target="#dialog" href="/reschedulebooking/{{record.booking_no.pk}}"><i class="fa fa-calendar  fa-2x mr-2 mr-2"></i>Reshedule</h5></a>
                  <a class="dropdown-item" style="color: blue;"  href="/SuccessView/{{record.booking_no.id}}"><i class="fa fa-eye fa-2x mr-2"></i>View</h5></a>
                </div>
              </li>
      </ul>
     {% endif %}
""")
    check= TemplateColumn(template_code=""" 
    <input name="selectaction" value={{record.pk}} type="checkbox" style="opacity:10;"></input> 
""")
    class Meta:
        model = Booking
        template_name = "b2bportal/common/bootstrap_htmx.html"
        fields = ['check','waybillno','booking_no__bookingref','booking_no__company_profile','origin_city', 'destination_city',
                  'booking_no__booking_status','booking_no__pickup_date', 'weight', 'shipment_type', 'action']


class bookingHTMxTableView(SingleTableMixin, FilterView):
    table_class = BookingHTMxTable
    filterset_class = BookingFilter
    
    paginate_by = 10
    #print(filterset_class)
    # CustomerWaybill = BookingFilter(request.GET, queryset=querySet )
  
    def get_queryset(self):
        qs= CustomerWaybill.objects.all()
        # qs= CustomerWaybill.objects.filter(booking_no__company_profile=GetCurrentCompany(self.request),booking_no__pickup_date__gte=date.today().isoformat(),booking_no__pickup_date__lte =date.today().isoformat()
        # ).order_by("-pickup_date")
        print('Rashmi queryset')
        return qs
       

    def get_action(self):
        bookingstatus=self.get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_shipments=self.get_queryset()
        under_process=all_shipments.count()
        submitted=all_shipments.filter(booking_no=1).count()
        un_submitted=0
        favourite=all_shipments.filter(booking_no__is_fav=True).count()
       
        # Add in a QuerySet of all the books

        context['under_process'] = under_process
        context['submitted'] = submitted
        context['un_submitted'] = un_submitted
        context['favourite'] = favourite
        base_template="b2bportal/base.html"
        context['base_template'] = base_template
      
        return context

    def get_template_names(self):
      
        if self.request.META.get('HTTP_HX_REQUEST'):
            template_name = "b2bportal/booking_table_partial.html"
        else:
            
            template_name = "b2bportal/booking.html"
        
        return template_name
    

def shipper_lookup(request):
    form=ShipmentBookingForm()
    data_list=shipper.objects.all()
    rows=""
    print(request.GET.get("selected_address",None))
    if "selected_address" in request.GET:
        print(request.GET["selected_address"])
        add=shipper.objects.get(pk=request.GET["selected_address"])
        address_data="{},{},{},{},{},{},{}".format(add.company_name,add.contact_person,add.address,add.country.name,add.city.name,add.mobile_number,add.pickup_point)
        data="""<input type="hidden" name="shipper" id="id_shipper" value={} />
               {}""".format(add.pk,address_data)
        return HttpResponse(data)
    
    if request.method == 'POST':
        company=GetCurrentCompany(request)
        print(request.POST)
        #get_current_company(request)
        if "search_data" in request.POST:
            search_data=request.POST.get("search_data")
            rows=""
            if search_data == "":
                data_list=shipper.objects.filter(CompanyProfile=company)
                print(data_list)
            else:
                data_list=data_list.filter(Q(address__icontains=search_data)|Q(company_name__icontains=search_data))
            for add in data_list:
                        address="{},{},{},{},{},{}".format(add.contact_person,add.address,add.country,add.city,add.mobile_number,add.pickup_point)
                        rows+="""
                                <tr hx-get="/shipper-lookup/?selected_address={}" data-dismiss="modal" hx-swap="innerHTML" hx-target="#selected_shipper" hx-trigger="click">
                                    <td></td>
                                    <td class="mailbox-name"><a class="naqel-text-color" href="#">{}</a></td>
                                    <td class="mailbox-subject"><a class="naqel-text-color" href="#">{}</a>
                                    </td>                                    
                                </tr>
            """.format(add.pk,add.company_name,address)
            return HttpResponse(rows)

    else:
        for add in data_list:
                        address="{},{},{},{},{},{}".format(add.contact_person,add.address,add.country,add.city,add.mobile_number,add.pickup_point)
                        rows+="""
                                <tr hx-get="/shipper-lookup/?selected_address={}" data-dismiss="modal" hx-swap="innerHTML" hx-target="#selected_shipper" hx-trigger="click">
                                    <td></td>
                                    <td class="mailbox-name"><a class="naqel-text-color" href="#">{}</a></td>
                                    <td class="mailbox-subject"><a class="naqel-text-color" href="#">{}</a>
                                    </td>
                                    
                                </tr>
            """.format(add.pk,add.company_name,address)

 
    return render(request, 'b2bportal/shipper_lookup.html', {
        'form':form,
        "address_data":format_html( rows)
})

def reciver_address_lookup(request):
    form=ShipmentBookingForm()
    data_list=consignee.objects.all()
    rows=""
    print(request.GET.get("selected_address reciver",None))
    if "selected_address" in request.GET:
        print(request.GET["selected_address"])
        add=consignee.objects.get(pk=request.GET["selected_address"])
        form= SelectedReceiverForm( initial={
            'company_name':add.company_name,
            'address':add.address,
            'contact_department':add.contact_person,
            'country':add.country,
            'city':add.city,
            'mobile':add.mobile_number,
            'state':add.pickup_point,
            'fax':add.email,
            'postal_code':add.zip_code, } )
        return render(request, 'b2bportal/selected_receiver.html', {
        'form':form,
        })
    
    if request.method == 'POST':
        print(request.POST)
        #get_current_company(request)
        if "search_reciver_data" in request.POST:
            search_reciver_data=request.POST.get("search_reciver_data")
            rows=""
            if search_reciver_data == "":
                data_list=consignee.objects.all()
            else:
                data_list=data_list.filter(Q(address__icontains=search_reciver_data)|Q(company_name__icontains=search_reciver_data))
            for add in data_list:
                        address="{},{},{},{},{},{}".format(add.contact_person,add.address,add.country,add.city,add.mobile_number,add.pickup_point)
                        rows+="""
                                <tr hx-get="/reciver-address-lookup/?selected_address={}" data-dismiss="modal" hx-swap="innerHTML" hx-target="#selected_reciver" hx-trigger="click">
                                    <td></td>
                                    <td class="mailbox-name"><a class="naqel-text-color" href="#">{}</a></td>
                                    <td class="mailbox-subject"><a class="naqel-text-color" href="#">{}</a>
                                    </td>                                    
                                </tr>
            """.format(add.pk,add.company_name,address)
            return HttpResponse(rows)

    else:
        for add in data_list:
                        address="{},{},{},{},{},{}".format(add.contact_person,add.address,add.country,add.city,add.mobile_number,add.pickup_point)
                        rows+="""
                                <tr hx-get="/reciver-address-lookup/?selected_address={}" data-dismiss="modal" hx-swap="innerHTML" hx-target="#selected_reciver" hx-trigger="click">
                                    <td></td>
                                    <td class="mailbox-name"><a class="naqel-text-color" href="#">{}</a></td>
                                    <td class="mailbox-subject"><a class="naqel-text-color" href="#">{}</a>
                                    </td>
                                    
                                </tr>
            """.format(add.pk,add.company_name,address)

 
    return render(request, 'b2bportal/reciver_address_lookup.html', {
        'form':form,
        "address_data":format_html( rows)
})
 

def dimensions(request):
    company=GetCurrentCompany(request)
    # booking_id=request.session["booking_id"]
    # if booking_id==None:
    #     dimensionsList=Dimensions.objects.filter(booking_id=booking_id)
    print('form',request.method)   
    form=DimensionsForm()
    if request.method == 'POST':
        form = DimensionsForm(request.POST)
        print('Print',form)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.company_profile=GetCurrentCompany(request)
            obj.save()  
            return HttpResponse(status=204)    
        else:
            print(form.errors)
            return HttpResponse(status=204)        
    return render(request, 'b2bportal/dimensions.html', {
        'form':form
})

def PrintBooking(request):

    print("HI",request.GET,request.POST)
    template_name=""
    filename=""
    context={

    }
    if request.method == 'POST':
        waybill_ids=request.POST.getlist("selectaction")
        waybill_list=Booking.objects.filter(id__in=waybill_ids)
        action=request.GET.get("action",None)
        template_name="WaybillLabelTemplate.ods"
         
        if waybill_list.count() > 0 :   
            #print(request.POST)
            
            if action.__contains__("print-sticker-A4"):
                    print ("print-sticker-A4")
                    template_name="WaybillLabelTemplateA5.ods"
                    filename="{0}.pdf".format("print-sticker-A4")
                    
            elif action.__contains__("print-sticker-A5"):
                    print ("print-sticker-A5")
                    filename="{0}.pdf".format("print-sticker-A5")
                    template_name="WaybillLabelTemplate.ods"
                
            elif action.__contains__("print-sticker-label"):
                    print ("print-sticker-label")
                    filename="{0}.pdf".format("print-sticker-label")
                    template_name="WaybillLabelTemplatesticker2.ods"

            context={
                        "data_list":waybill_list
                    }
            
            base64_string= generate_report_document_base64(request,template_name,filename,context)
           
            return HttpResponse(base64_string,status=409)
        else:
            print('Not Selected')    
            # content = {'please move along': 'nothing to see here'}
            # return HttpResponse(content, status=204)


            # response = TemplateResponse(request, 'b2bportal/password_reset_done.html', {})
            # Register the callback
            # response.add_post_render_callback(my_render_callback)

            # opts = model._meta
            # templates = ["%s/print.html" % (opts.model_name), "base/print.html"]               
            return HttpResponseRedirect('/booking/',{'message':'Rashmi'}, {'message':'CSK'})
            # return TemplateResponse(request, 'b2bportal/password_reset_done.html', {'message': 'Please select atleast one waybill number.', })
            # return HttpResponse('No Waybill selected')          
            # return HttpResponse(status=204)  
            # return redirect(reverse("/b2bportal/booking"), {"alert":"My Alert"})        
        
    else:
        return generate_report_document(request,template_name,filename,context)
    
def add_new_shipper(request):
    form=AddNewShipperForm()
    if request.method == 'POST':
        
        form = AddNewShipperForm(request.POST)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.company_profile=GetCurrentCompany(request)
            obj.save()
            address_data="{},{},{},{},{},{}".format(obj.contact_person,obj.address,obj.country.name,obj.city.name,obj.mobile_number,obj.pickup_point)
            data="""<input type="hidden" name="shipper" id="id_shipper" value={} />
                {}""".format(obj.pk,address_data)
            print(data)    
            return HttpResponse(data)
        else:
            print(form.errors)
            return HttpResponse(status=204)

         
    return render(request, 'b2bportal/add_new_shipper.html', {
        'form':form
})
# def SuccessView(request,booking_id):
#     waybill_list=Booking.objects.filter(id=booking_id)
#     print('waybill_list',waybill_list)
#     if waybill_list.count() > 0:
#         company=GetCurrentCompany(request)
#         booking=waybill_list[0]
#         return render(request, 'b2bportal/confirm.html', {
#                 'booking': booking,
#                 'waybills': waybill_list,
#                 'company': company,
#             })
#     else:
#         return HttpResponse(status=204)
    
def reschedulebooking(request,id):
    booking = Booking.objects.get(id=id)
   
    if request.method == "POST":
        form = reschedulebookingForm(request.POST)
        if form.is_valid():
            print("test",request.method)
            object_Booking = Booking.objects.get(id=id)
            form = reschedulebookingForm(request.POST, instance=object_Booking)
            form.save()
            message='{"ShowMessage":"'+"{}".format(format_html("<h6 class='text-success'>Booking #{} Reschedule Successfully </h6>".format(object_Booking.bookingref))) +'"}' 
            return HttpResponse(status=204, headers={
                            "HX-Trigger" : message,
            })
             
        else:
            print(form.errors)
    else:
        print("else dsfsdfsdf out")
        form = reschedulebookingForm()

    return render(request, 'b2bportal/reschedulebooking.html', {
        'form': form,
        'booking':booking,
    })

def deletebooking(request,id):
    if request.method == "GET":
        wbillno=Booking.objects.filter(id=id)
        bk=Booking.objects.get(id=id)
        if bk:
            wbillno.delete()
            bk.delete()
        return HttpResponse(status=204)
def alertnotification(request,booking_id,alert_type):
    book1=Booking.objects.get(pk=booking_id)
    print('alert',booking_id)
    message="Push"
    if alert_type==1:
        book1.is_SMS=True
        message="SMS"
    elif alert_type==2:
        book1.is_Push=True
        message="Push"
    elif alert_type==3:
        book1.is_Email=True
        message="Email"
    book1.save()  

    return HttpResponse("<i class='fa fa-check mr-2 mr-2'></i>"+message) 


def newbooking(request,booking_id):
    waybill=None
    booking=None 
    company=GetCurrentCompany(request)
    default_shipper=shipper.objects.filter(is_default=True,company_profile=company).first()
    print('default_shipper',default_shipper)
    
    try:        
                
                records=[]
                ClientID=request.session['clientID']
                print(ClientID)
                task = {"ClientID": ClientID}
                Webapilink = 'http://212.107.118.74:81/b2b/api/b2b/getActiveloadType'
                resp = requests.get(Webapilink, data=task)
                records = resp.json()
                print('loadtype records',records)
                for data in records:
                    print('shipmentType',data["Name"])
    except:
            pass
    print('Client ID',request.session['clientID'])
    if request.session['clientID'] is not None:
        #shipment_type = shipmenttype.objects.filter(shipment_id__in=(str(data["ID"])))
        shipment_type = shipmenttype.objects.filter(name=data["Name"])
        print('Loadtype',shipment_type)
    form=ShipmentBookingForm()
    form.fields["shipment_type"].queryset=shipment_type
    
    
    if request.method == 'GET':
        if booking_id > 0:
            booking=Booking.objects.get(pk=booking_id)
            if booking:    
                    form = ShipmentBookingForm(initial={
                        'company_name':company.company_name, 
                        'contact_person':booking.shipper.contact_person,
                        'country':booking.shipper.country,
                        'city':booking.shipper.city,
                        'address':booking.shipper.address,
                        'mobile':booking.shipper.mobile_number, 
                        'mobile':booking.shipper.contact_number,
                        'company_name':booking.consignee.company_name,
                        'address':booking.consignee.address,
                        'contact_department':booking.consignee.contact_person,
                        'mobile':booking.consignee.mobile_number,
                        'country':booking.consignee.country,
                        'city':booking.consignee.city,
                        'state':booking.consignee.pickup_point,
                        'postal_code':booking.consignee.zip_code,
                        'fax':booking.consignee.email,
                        'shipment_type':booking.shipment_type,
                        'payment_method':booking.payment_method,
                        'piece_count':booking.piece_count,
                        'chargable_weight':booking.chargable_weight,
                        'gross_weight':booking.gross_weight,
                        'pickup_date':strftime('%Y-%m-%d'),
                        'pickup_time':strftime('%Y-%m-%d'),
                        'customs_value':booking.customs_value, 
                        'additonal_services': booking.additonal_services,
                        'goods_description': booking.goods_description,
                        'insurance_value': booking.insurance_value,
                        'declare_value': booking.declare_value,
                    })
            
    if request.method == 'POST':
        default_shipper=shipper.objects.filter(is_default=True,company_profile=company).first()
        form = ShipmentBookingForm(request.POST)
        print(form.errors)
        if form.is_valid():
            con=consignee.objects.create(
                company_name=company,
                contact_person=form.cleaned_data['contact_department'],
                contact_number=form.cleaned_data['mobile'],
                mobile_number=form.cleaned_data['mobile'],
                address=form.cleaned_data['address'],
                country=form.cleaned_data['country'],
                city=form.cleaned_data['city'],
                pickup_point=form.cleaned_data['state'],
                email=form.cleaned_data['fax'],
                zip_code=form.cleaned_data['postal_code'],
            )
            con.save()
            
            obj=form.save(commit=False)
            obj.shipper=default_shipper
            obj.company_profile=GetCurrentCompany(request)
            obj.consignee=con
            obj.pickup_date = datetime.date.today()
            obj.pickup_time = datetime.time()
            obj.save()
            data=form.save()
            booking = Booking.objects.get(id=data.id)
            print(form.base_fields["save_to_addressbook"])
            # if obj.save_to_addressbook == True:
            #     print(obj.address)
                #consig=consignee.create(request,obj.company_profile,)

            print('data',booking)
            

        return render(request, 'b2bportal/success.html', {
        'booking': booking,
        'company': company,
        'shipper':default_shipper,
        })
        
    return render(request, 'b2bportal/newbooking.html', {
        'form':form,
        'records':records,
        'shipper':default_shipper,

})


def BookingView(request):
    
    start_date=request.GET.get("start_date","")
    end_date=request.GET.get("end_date","")
    query=request.GET.get("query","")
    request.session["start_date"]=start_date
    request.session["end_date"]=end_date
    request.session["query"]=query
    
    if "start_date" in request.GET:
          
        if start_date == "" or end_date == "":
            del request.session["start_date"] 
            del request.session["end_date"] 
        
        if query == "":
            del request.session["query"] 
        
        return booking_list(request)
  
    else:
        #request.session["start_date"]=request.GET["start_date"]
        #print('Start date'.request.GET["start_date"])
        
        shipment_list_qs = Booking.objects.all().order_by('id')
        filter_qs=BookingFilter(request.GET,shipment_list_qs)
        if request.htmx:
            base_template="b2bportal/_partial.html"
        else:
            base_template="b2bportal/base.html"
    
        return render(request, "b2bportal/booking_list.html", { "base_template":base_template,'filter':filter_qs})

def booking_list(request):
   

    start_date=request.session.get("start_date","")
    end_date=request.session.get("end_date","")
    query=request.session.get("query","")

    shipment_list_qs = Booking.objects.all().order_by('-waybillno')

    if start_date != "" and end_date !="":
        start_date=datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date=datetime.datetime.strptime(end_date, "%Y-%m-%d")
        shipment_list_qs = Booking.objects.filter(booking_date__range=[start_date,end_date]).order_by('-waybillno')
    
    if query != "":
        print("que2ry",query)
        shipment_list_qs=shipment_list_qs.filter(Q(waybillno__icontains=query) | Q(bookingref__icontains=query))
    
    filter_qs=BookingFilter(request.GET,shipment_list_qs)
    filter_qs_form=filter_qs 
    count=Booking.objects.count()
    print('Booking Count',count)

    filter_qs=filter_qs.qs
    paginator = Paginator(filter_qs, 7)  #  paginate_by 5
    page = request.GET.get('page')
   
    base_template = "b2bportal/booking.html"
    if request.htmx:
        base_template="b2bportal/_partial.html"
    else:
        base_template="b2bportal/base.html"
  
    try:
        shipment_list = paginator.page(page)
    except PageNotAnInteger:
        shipment_list = paginator.page(1)
    except EmptyPage:
        shipment_list = paginator.page(paginator.num_pages)
  
    return render(request, "b2bportal/booking_list_htmx.html", {"booking_list": shipment_list,"base_template":base_template,"filter":filter_qs_form,})


def b2blogin(request):
    """Renders the Service page."""
    
    if request.method == 'POST':
        form = B2BLoginForm(request.POST)
        print(request.POST.get('username'))
        user = NaqelUser.objects.filter(
            email=request.POST.get('username')).first()
        print("Username", user.username)
        if user is not None:
            username = user.username
            password = request.POST.get('password')
            user = authenticate(username=user.username, password=password)

            if user is not None:
                login(request, user)
                company=GetCurrentCompany(request)
                request.session['company'] = company.company_name
                request.session['clientID'] = company.client_id
                request.session['user'] = user.email
                return redirect('/home')
            else:
                print("error")
                messages.error(
                    request, "Enter a valid UserName and password")
        else:
            messages.error(
                request, "Enter a valid UserName and password")
            print(form)
            form = B2BLoginForm()

    else:
        print("error-else")
        form = B2BLoginForm()
    return render(request, 'b2bportal/login.html', {
        'form': form,
        })


def clientreport(request):
    print("ClientReportPage")
    if request.method == 'POST':
        report_type=request.POST.get("reportType")
        filename="{0}.pdf".format(report_type)
        if "btnpdf" in request.POST:
            filename="{0}.pdf".format(report_type)
            print("hi")

        elif "btnexcel" in request.POST:
            filename="{0}.xlsx".format(report_type)

        elif "btncsv" in request.POST:
            filename="{0}.csv".format(report_type)    
         
            
        fromdate=request.POST.get("from_date")
        todate=request.POST.get("to_date")
        company=GetCurrentCompany(request)
        ClientID=company.client_id
        form = ClientForm(request.POST)
        data=None
       
        try:
            Webapilink=None
            task=None

            if report_type == "Daily Recap":
                task = {"StartDate": fromdate, "EndDate": todate, "ClientID": ClientID}
                Webapilink = 'http://212.107.118.74:81/b2b/daily-recap-get'
                template_name="DailyRecap.ods"

            elif report_type == "Delivery":
                task = {"StartDate":fromdate, "EndDate": todate, "ClientID": ClientID}
                Webapilink = 'http://212.107.118.74:81/b2b/delivery-get'
                template_name="Delivery.ods"

            elif report_type == "Waybill Last Status":
                task = {"StartDate": fromdate, "EndDate": todate, "ClientID": ClientID}
                Webapilink = 'http://212.107.118.74:81/b2b/daily-recap-get'
                template_name="WayBillLastStatus.ods"


            elif report_type == "Customer KPI":
                task = {"StartDate":fromdate, "EndDate": todate, "ClientID": ClientID}
                Webapilink = 'http://212.107.118.74:81/b2b/customer-kpi-get'
                template_name="CustomerKpi.ods"


            elif report_type == "Multiple Shipment Tracking":
                task = {"StartDate": fromdate, "EndDate": todate, "ClientID": ClientID}
                Webapilink = 'http://212.107.118.74:81/b2b/multi-tracking-get'
                template_name="Multi.ods"


            elif report_type == "Complete Tracking":
                task = {"StartDate": fromdate, "EndDate": todate, "ClientID": ClientID}
                Webapilink = 'http://212.107.118.74:81/b2b/multi-tracking-get'
                template_name="CompleteTracking.ods"  

            elif report_type == "Delivery Performance":
                task = {"StartDate": fromdate, "EndDate": todate, "ClientID": ClientID}
                Webapilink = 'http://212.107.118.74:81/b2b/delivery-performance-client-get'
                template_name="DeliveryPerformance.ods"  

            elif report_type == "Proof Of Delivery (POD) Report":
                task = {"StartDate": fromdate, "EndDate":todate, "ClientID": ClientID}
                Webapilink = 'http://212.107.118.74:81/b2b/customer-portal-pod-get'
                template_name="PodReport.ods"  


            elif report_type == "Shipments Status":
                task = {"StartDate": fromdate, "EndDate":todate, "ClientID": ClientID}
                Webapilink = 'http://212.107.118.74:81/b2b/daily-report-client-status-get'
                template_name="Shipment.ods" 


            elif report_type == "Delivery Recap":
                task = {"StartDate":fromdate, "EndDate":todate, "ClientID": ClientID}
                Webapilink = 'http://212.107.118.74:81/b2b/delivery-recap-get'
                template_name="DeliveryRecap.ods"  

            elif report_type == "Service Level Report":
                task = {"StartDate": fromdate, "EndDate":todate, "ClientID": ClientID}
                Webapilink = 'http://212.107.118.74:81/b2b/sl-web-client-occ-get'
                template_name="ServiceLevelReport.ods"

            elif report_type == "Service Level Ratio":
                task = {"StartDate":fromdate, "EndDate":todate, "ClientID": ClientID}
                Webapilink = 'http://212.107.118.74:81/b2b/sl-web-client-occ-get'
                template_name="ServiceLevelRatio.ods"        
    

            if Webapilink and task :
                resp = requests.post(Webapilink, data=task)
                data = resp.json()
        except:
            pass
        
        


        if data == None:
            context={}
        else:
            context={
                "data_list":data["Result"]
            }


        
        return generate_report_document(request,template_name,filename,context)
        """return render(request, 'b2bportal/clientreport.html', {
                'client': client_items,
                'form': form,
                'title': 'Client Report',
                'data_list':data,
               

            })"""
    
    else:

        form = ClientForm()
        return render(request, 'b2bportal/clientreport.html', {
            'form': form,
            'title': 'Client Report',
            
        })


def deleteUploadBooking(request,id):
    if request.method == "GET":
        uploadDelete=UploadStaging.objects.filter(pk=id)
        uploadDelete.delete()
        return redirect("/UploadBooking")

def handle_uploaded_file(f):
    with open('b2bportal/files/upload_excel-booking.xlsx', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
class UploadData:
    pass
def UploadBooking(request):
    company=GetCurrentCompany(request)
    waybill_count=0
    if request.method == 'POST':
        records=[]
        
        if 'UploadFile' in request.POST:
            if len(request.FILES) > 0:
                print("hi dfdf")
                attachment=request.FILES['file']
                try:
                    UploadStaging.objects.filter(sessionUserID=request.session._session_key).delete()
                    dataset = Dataset()
                    exceldata = attachment
                    imported_data = dataset.load(exceldata.read())
                    for data in imported_data:
                        
                        row=UploadStaging.objects.create()
                        row.refno=data[0]
                        row.origin=data[1]
                        row.Destination=data[2]
                        row.Name=data[3]
                        row.Email=data[4]
                        row.PhoneNo=data[5]
                        row.MobileNo=data[6]
                        row.Address=data[7]
                        row.Location=data[8]
                        row.POBox=data[9]
                        
                        #row.Date=datetime.strftime(data[10],'%d-%m-%Y')
                        row.Peices=int(data[11])
                        row.Weight=float(data[12])
                        row.Width=float(data[13])
                        row.Length=float(data[14])
                        row.Height=float(data[15])
                        
                        row.CODAmount=float(data[16])
                        print('excel after row')
                        row.DeliveryInstruction=data[17]
                        row.PODType=data[18]
                        
                        row.DeclaredValue=float(data[19])
                        row.GoodDesc=data[20]
                        row.ConsigneeNationalID=data[21]
                        row.message=""
                        row.sessionUserID=request.session._session_key
                        

                        if city.objects.filter(name=row.origin).count()== 0:
                            row.message=row.message+"Error Origin City |"
                        if city.objects.filter(name=row.Destination).count()== 0:
                            
                            row.message=row.message+"Error Dest City |"
                        if row.MobileNo=="":
                            row.message=row.message+" Mobile No |"
                        if row.Peices==0:
                            row.message=row.message+" 0 Peice |"
                        print('row data',row)    
                    


                        row.save()
                        print('All Data',data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],data[17],data[18],data[19],data[20],data[21])
                    
                            
                except (ValueError, TypeError):
                        print(ValueError,TypeError)
                        pass  # invalid input from the client; ignore and fallback to empty City queryset
                records=UploadStaging.objects.filter(sessionUserID=request.session._session_key)
                validdata=records.filter(message="").count()                
                return render(request,'b2bportal/UploadBooking.html',context={"records":records,
                "valid":validdata,
                "notvalid":records.count()-validdata
                })
            else:
                records=UploadStaging.objects.filter(sessionUserID=request.session._session_key)
                validdata=records.filter(message="").count()                
                return render(request,'b2bportal/UploadBooking.html',context={"records":records,
                "valid":validdata,
                "notvalid":records.count()-validdata
                })
           
        elif 'generate_waybill' in request.POST:
            records=UploadStaging.objects.filter(sessionUserID=request.session._session_key)
            print('record',records)
            validdata=records.filter(message="") 
            
            booking=None

           
            for rec in validdata:
                waybill_count=waybill_count+1
                if booking==None: 
                    booking=Booking.objects.create()
                    booking.company_profile=company
                    booking.is_fav=False
                    print('booking',booking)
                    booking.save()
                
                new_waybill=Booking.objects.create()
                new_waybill.company_profile=company
                # new_waybill.contact_number = company.phone_number
                # new_waybill.contact_number = company.phone_number
                # new_waybill.origin_city=city.objects.filter(name= rec.origin).first()
                # print('city data',city.objects.filter(name= rec.origin).first())
                new_waybill.waybillno=next(WaybillNumber)
                new_waybill.piece_count=rec.Peices
                #for barcode 
                for b in range(1,new_waybill.piece_count+1):
                    barcode_data="{:05d}".format(b)
                    obj=BarcodeCount.objects.create(
                        waybillno=new_waybill,
                        barcode_number="{}{}".format(new_waybill.waybillno,barcode_data)
                    )
                    obj.save()
                # new_waybill.booking_no=booking
                # new_waybill.refrenceno=rec.refno
                
                new_waybill.gross_weight=rec.Weight
                #new_waybill.=city.objects.filter(name= rec.Destination).first()
                # new_waybill.width=rec.Width
                # new_waybill.delivery_instruction=rec.DeliveryInstruction
                new_waybill.booking_date=datetime.date.today()
                # #new_waybill.pod_type=rec.PODType
                # new_waybill.declare_value=rec.DeclaredValue
                new_waybill.custom_value=rec.CODAmount
                # new_waybill.cust_national_id=rec.ConsigneeNationalID
                
                con = consignee.objects.create()
                con.contact_person = rec.Name
                con.address = rec.Address
                con.address = "{},{}".format(rec.Location,rec.POBox)
                con.email = rec.Email
                con.mobile_number = rec.MobileNo
                con.mobile_number=rec.PhoneNo
                con.is_inactive=True
                con.save()

                new_waybill.consignee=con
                #new_waybill.shipper__city=city.objects.filter(name= rec.origin).first() 
                #new_waybill.destination_city=city.objects.filter(name= rec.Destination).first() 
                print('All data',new_waybill)
                new_waybill.save()
              
            validdata.delete()
            records=UploadStaging.objects.filter(sessionUserID=request.session._session_key)
            validdata=records.filter(message="").count() 

            return render(request,'b2bportal/UploadBooking.html',context={"records":records,
                "waybill_count":waybill_count,
                "valid":validdata,
                "notvalid":records.count()-validdata
                })
    else:
            records=UploadStaging.objects.filter(sessionUserID=request.session._session_key)
            validdata=records.filter(message="").count() 
            return render(request,'b2bportal/UploadBooking.html',context={"records":records,
                "valid":validdata,
                "notvalid":records.count()-validdata
                })        
#Views
