
from argparse import Action
from asyncore import read
from cProfile import label
from cgitb import text 
from ensurepip import bootstrap
from pickle import READONLY_BUFFER
from time import strftime
from xml.dom.minidom import ReadOnlySequentialNamedNodeMap
from django import forms
from core.models import *
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout , Div,Row,HTML
from django.core.exceptions import ValidationError
from django.urls import reverse
from dal import autocomplete
from django.contrib.admin.widgets import AutocompleteSelect
import datetime
from .booking import Booking
#from phonenumber_field.formfields import PhoneNumberField
#from phonenumber_field.widgets import PhoneNumberPrefixWidget

class B2BLoginForm(forms.Form):
    username = forms.CharField(
         widget=forms.TextInput({'class': 'form-control', }))
    password = forms.CharField(
        widget=forms.PasswordInput({'class': 'form-control', }))


 

#Registration
class B2BRegisterationForm(forms.ModelForm):
    ComName = forms.CharField(label=_("Company Name"), max_length=100,help_text='Required',required=True,widget= forms.TextInput({'class':'form-control','placeholder':_('Company Name *')}))
    CustomerName = forms.CharField(label=_("Customer Name"), max_length=100,help_text='Required',widget= forms.TextInput({'class':'form-control','placeholder':_('Customer Name *')}))
    IndType = forms.ModelChoiceField(queryset=IndustryType.objects.all(),empty_label='Industry Type *', widget= forms.Select({'class': 'form-control','placeholder':_('Industry Type') }))
    MoNumber= forms.CharField(label=_("Mobile Number"), max_length=100,help_text='Required',required=True,widget= forms.TextInput({'class':'form-control','placeholder':_('Mobile Number *') }))
    Email =  forms.EmailField(label=_("Email "), max_length=200,help_text='Required',required=True,widget=forms.EmailInput({'class': 'form-control','placeholder':_('Email *')}))
    Address= forms.CharField(label=_("Address"), max_length=100,help_text='Required',required=True,widget= forms.TextInput({'class':'form-control','placeholder':_('Address *')}))
    City =forms.ModelChoiceField(queryset=city.objects.all(),empty_label='City *',label=_("City"),help_text='Required',required=True,widget= forms.Select({'class':'form-control','placeholder':_('City')}))
    Country =forms.ModelChoiceField(queryset=country.objects.all(),empty_label='Country *',label=_("Country"),help_text='Required',required=True,widget= forms.Select({'class':'form-control','placeholder':_('Country')}))


    class Meta:
        model = B2BRegisteration
        fields=('ComName', 'CustomerName', 'IndType','MoNumber','Email','Address','City','Country')
    def clean(self):
        cleaned_data = super().clean()
        cc_myself = cleaned_data.get("MoNumber")

        if cc_myself :
            # Only do something if both fields are valid so far.
            ph_num = cc_myself
            print(ph_num)
            # Validation --> Check if number length is greater or less then 10
            if len(ph_num) > 10 or len(ph_num) < 10:
                raise ValidationError('Phone number is not valid (Enter a 10 digit number)')
            else:
                # Check if first number is 0
                if ph_num[0] == '0':
                    try:
                        ph_con_num = float(ph_num)
                        #raise ValidationError("ENQ - Your phone number is valid")
                    except:
                        raise ValidationError('Phone number is not valid (A number should not contain any characters)')
                else:
                    raise ValidationError(" Phone number is not valid (A number should start with 0)")
#endvalidation 

class TrackingForm(forms.Form):
    waybills = forms.CharField(label=_("Waybill Numbers"), max_length=300, help_text='Required',
                               widget=forms.Textarea({
                                   'class': 'form-control form-control-sm',
                                   'rows': 5,
                                   'width': '100%',
                                   'placeholder': _('Please enter multiple waybills separated by comma.')}))

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

class EnquiryModuleForm (forms.ModelForm):
    Name= forms.CharField(label=_("Full Name"), max_length=100,help_text='Required',required=True,widget= forms.TextInput({'class':'form-control','placeholder':_('Name')}))
    Email =  forms.EmailField(label=_("Email "), max_length=200,help_text='Required',required=True,widget=forms.EmailInput({'class': 'form-control','placeholder':_('E-mail Address')}))
    PhoneNo =  forms.CharField(label=_("PhoneNo "), max_length=200,help_text='Required',required=True,widget=forms.TextInput({'class': 'form-control','placeholder':_('Phone Number')}))
    # EnquiryType=forms.ModelChoiceField(queryset=EnquiryType.objects.all(),widget= forms.Select({'class': 'form-control','placeholder':_('Reason') }))
    Details =forms.CharField(label=_("Details"), max_length=500,help_text='Required',required=True,widget= forms.Textarea({'class':'form-control'}))

    class Meta:
        model = EnquiryModule
        fields=('Name', 'Email', 'PhoneNo','Details')
    def clean(self):
        cleaned_data = super().clean()
        cc_myself = cleaned_data.get("PhoneNo")

        if cc_myself :
            # Only do something if both fields are valid so far.
            ph_num = cc_myself
            print(ph_num)
            # Validation --> Check if number length is greater or less then 10
            if len(ph_num) > 10 or len(ph_num) < 10:
                raise ValidationError('ENQ - Phone number is not valid (Enter a 10 digit number)')
            else:
                # Check if first number is 0
                if ph_num[0] == '0':
                    try:
                        ph_con_num = float(ph_num)
                        #raise ValidationError("ENQ - Your phone number is valid")
                    except:
                        raise ValidationError('ENQ - Phone number is not valid (A number should not contain any characters)')
                else:
                    raise ValidationError("ENQ - Phone number is not valid (A number should start with 0)")
#endvalidation           

class ComplaintsModuleForm (forms.ModelForm):
    Name= forms.CharField(label=_("Full Name"), max_length=100,help_text='Required',required=True,widget= forms.TextInput({'class':'form-control','placeholder':_('Name')}))
    Email =  forms.EmailField(label=_("Email "), max_length=200,help_text='Required',required=True,widget=forms.EmailInput({'class': 'form-control','placeholder':_('E-mail Address')}))
    PhoneNo =  forms.CharField(label=_("PhoneNo "), max_length=200,help_text='Required',required=True,widget=forms.TextInput({'class': 'form-control','placeholder':_('Phone Number')}))
    Reason=forms.ModelChoiceField(queryset=ComplaintsType.objects.all(),widget= forms.Select({'class': 'form-control','placeholder':_('Reason') }))
    Details =forms.CharField(label=_("Details"), max_length=500,help_text='Required',required=True,widget= forms.Textarea({'class':'form-control'}))
    evidence=forms.FileField(required=False,widget= forms.FileInput({'class':'form-control'}))

    class Meta:
     model = ComplaintsModule
     fields=('Name', 'Email', 'PhoneNo','Reason','Details','evidence')  
    def clean(self):
        cleaned_data = super().clean()
        cc_myself = cleaned_data.get("PhoneNo")

        if cc_myself :
            # Only do something if both fields are valid so far.
            ph_num = cc_myself
            print(ph_num)
            # Validation --> Check if number length is greater or less then 10
            if len(ph_num) > 10 or len(ph_num) < 10:
                raise ValidationError('COMP - Phone number is not valid (Enter a 10 digit number)')
            else:
                # Check if first number is 0
                if ph_num[0] == '0':
                    try:
                        ph_con_num = float(ph_num)
                        #raise ValidationError("COMP - Your phone number is valid")
                    except:
                        raise ValidationError('COMP - Phone number is not valid (A number should not contain any characters)')
                else:
                    raise ValidationError("COMP - Phone umber is not valid (A number should start with 0)")
#endvalidation    

class reschedulebookingForm (forms.ModelForm):

    pickup_date= forms.DateField(label="pickup_date",
                                  widget=forms.DateInput(attrs={'placeholder': _('Pick A Date'), 'type': 'date','class': 'form-control placeholdercolor'}))
    pickup_time= forms.TimeField(label="from_time",

                                  widget=forms.TimeInput(attrs={'placeholder': _('Pick A time'), 'type': 'time','class': 'form-control placeholdercolor'}))
    OfficeUpto =forms.TimeField(label="To_time",

                                  widget=forms.TimeInput(attrs={'placeholder': _('Pick A time'), 'type': 'time','class': 'form-control placeholdercolor'}))
    SchedulingReason=forms.ModelChoiceField(queryset=SchedulingReason.objects.all(),widget= forms.Select({'class': 'form-control','placeholder':_('Reason') }))      

    class Meta:
     model = Booking
     fields=('pickup_date', 'pickup_time', 'OfficeUpto','SchedulingReason')


class ClientForm(forms.Form):

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
        
class DashboardForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DashboardForm, self).__init__(*args, **kwargs)
        self.fields['from_date'].initial = date.today
        self.fields['to_date'].initial = date.today
 
    from_date= forms.DateField(label="From Date",
                                  widget=forms.DateInput(attrs={'placeholder': _('From Date'), 'type': 'date','class': 'form-control placeholdercolor'}))
    to_date= forms.DateField(label="To Date",
                                  widget=forms.DateInput(attrs={'placeholder': _('To Date'), 'type': 'date','class': 'form-control placeholdercolor'}))

class EDDNewForm (forms.Form):
    def __init__(self, *args, **kwargs):
        super(EDDNewForm, self).__init__(*args, **kwargs)
        self.fields['from_date'].initial = date.today
        self.fields['time'].initial = date.today
    
    def clean_shortcodeurl(self):
        data = self.cleaned_data['Weight']
        if "my_custom_example_url" not in data:
            raise ValidationError("my_custom_example_url has to be in the provided data.")
        return data
    

    from_date= forms.DateField(required=False,  widget=forms.DateInput(
        attrs={
            'type': 'date',
            'class': 'form-control',
        }
    )) 
    time =  forms.TimeField(required=False, initial=strftime("%I:%M %p"),  widget=forms.TimeInput(
        attrs={
            'type': 'time',
            'class': 'form-control',

        }
    ))
    originCountry = forms.ModelChoiceField(queryset=country.objects.all(),widget=forms.Select({'class': 'form-control form-control-sm',
    'onchange':'postdata(this,"origin_country");',
     }))
     
    OriginCity =forms.ModelChoiceField(queryset=city.objects.all(),widget=forms.Select({'class': 'form-control form-control-sm', }))
    serviceType =forms.ModelChoiceField(queryset=StandardCode.objects.filter(CodeType='ServiceType'),widget=forms.Select({'class': 'form-control form-control-sm', }))
    Weight =forms.DecimalField(widget=forms.Select({'class': 'form-control form-control-sm', }))
    destinationCountry =forms.ModelChoiceField(queryset=country.objects.all(),widget=forms.Select({'class': 'form-control form-control-sm',
    'onchange':'postdata(this,"destination_country");',
    
     }))
    DestinationCity =forms.ModelChoiceField(queryset=city.objects.all(),widget=forms.Select({'class': 'form-control form-control-sm', }))
    productType =forms.ModelChoiceField(queryset=StandardCode.objects.filter(CodeType='ProductType'),widget=forms.Select({'class': 'form-control form-control-sm', }))
    

class EDDForm (forms.Form):
    def __init__(self, *args, **kwargs):
        super(EDDForm, self).__init__(*args, **kwargs)
        self.fields['from_date'].initial = date.today
        self.fields['time'].initial = date.today

    from_date= forms.DateField(required=False,  widget=forms.DateInput(
        attrs={
            'type': 'date',
            'class': 'form-control',
        }
    )) 
    time =  forms.TimeField(required=False, initial=strftime("%I:%M %p"),  widget=forms.TimeInput(
        attrs={
            'type': 'time',
            'class': 'form-control',

        }
    ))
    #originCountry =forms.ModelChoiceField(queryset=country.objects.all(),
    #widget=AutocompleteSelect(EstimatedDeliveryDuration._meta.get_field('originCountry').remote_field, admin.site)
    originCountry =forms.ModelChoiceField(queryset=country.objects.all(),widget=forms.Select({'class': 'form-control form-control-sm',}))
     
    originCity =forms.ModelChoiceField(queryset=city.objects.all(),widget=forms.Select({'class': 'form-control form-control-sm', }))
    serviceType =forms.ModelChoiceField(queryset=StandardCode.objects.filter(CodeType='ServiceType'),widget=forms.Select({'class': 'form-control form-control-sm', }))
    weight =forms.DecimalField()
    destinationCountry =forms.ModelChoiceField(queryset=country.objects.all(),widget=forms.Select({'class': 'form-control form-control-sm', }))
    destinationCity =forms.ModelChoiceField(queryset=city.objects.all(),widget=forms.Select({'class': 'form-control form-control-sm', }))
    productType =forms.ModelChoiceField(queryset=StandardCode.objects.filter(CodeType='ProductType'),widget=forms.Select({'class': 'form-control form-control-sm', }))
     

class PasswordResetCustomForm(forms.Form):
    email = forms.CharField(
        required=False,
        label=_("Email"),
        max_length=254,
        widget=forms.TextInput()
    ) 
    phone = forms.CharField(
       required=False,
        label=_("PhoneNumber"),
        max_length=254,
        widget=forms.TextInput(attrs={'id':'phone' ,'type':'tel' ,'name':'phone' ,'class': 'form-control'}))


    
class InvoiceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields['from_date'].initial = date.today
        self.fields['to_date'].initial = date.today
   
    

    from_date= forms.DateField(label="From Date",
                                  widget=forms.DateInput(attrs={'placeholder': _('From Date'), 'type': 'date','class': 'form-control placeholdercolor'}),required=True)
    to_date= forms.DateField(label="To Date",
                                  widget=forms.DateInput(attrs={'placeholder': _('To Date'), 'type': 'date','class': 'form-control placeholdercolor'}),required=True)

Choices = (
    ('0', _('Documents')),
    ('1', _('Non-Documents')),
)


EnglishLevel = (
    ('Beginner', _('Beginner')),
    ('Intermediate', _('Intermediate')),
    ('Native', _('Native')),
)

class RateCalForm(forms.Form):
    shipping_from_country = forms.ModelChoiceField(queryset=country.objects.all(),empty_label=_('From Country'),widget=forms.Select({'class': 'form-control form-control-sm',}))
    shipping_to_country = forms.ModelChoiceField(queryset=country.objects.all(),empty_label=_('To Country'),widget=forms.Select({'class': 'form-control form-control-sm',}))
    shipping_from_city =forms.ModelChoiceField(queryset=city.objects.all(),empty_label=_('From City'),widget=forms.Select({'class': 'form-control form-control-sm', }))
    shipping_to_city = forms.ModelChoiceField(queryset=city.objects.all(),empty_label=_('To City'),widget=forms.Select({'class': 'form-control form-control-sm', }))

    product = forms.ModelChoiceField(queryset=StandardCode.objects.filter(CodeType='ProductType'),widget=forms.Select({'class': 'form-control form-control-sm', }))
    piece_count = forms.IntegerField(label="Piece Count",
                                     widget=forms.NumberInput(attrs={'placeholder': _('Piece Count'), }))
    Weight = forms.IntegerField(
        widget=forms.TextInput(attrs={'placeholder': _('Weight KG'), 'class': 'form-control' }))
    
    is_document = forms.ChoiceField(required=False,
        widget=forms.RadioSelect(attrs={
            'display': 'inline-block',
        }),
        choices=Choices
    )
   
    
     




