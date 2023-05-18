from email.policy import default
from itertools import count
import string
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager
from django.core.validators import RegexValidator
from datetime import datetime
from django.forms import IntegerField
from django.utils.translation import gettext_lazy as _
from psycopg2 import IntegrityError
from tinymce.models import HTMLField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
#from .EmailUtility import send_html_mail
from django_pgviews import view as pg
from datetime import date
from tinymce.models import HTMLField
from django.utils.timezone import now
# Create your models here.

BOOKING_STATUS = [
    ('Booked', 'Booked'),
    ('Courier-Informed', 'Courier-Informed'),
    ('Cancel-Booking', 'Cancel-Booking'),
    ('Scheduled', 'Scheduled'),
    ('Picked-Up','Picked-Up'),
    ('Miss-PickUp','Miss-PickUp'),
    ('Acknowledge','Acknowledge'),   
]
PAYMENT_METHOD = [
    ('Cash', 'Cash'),
    ('Credit-card', 'Credit-card'),
    ('Shipper-Account', 'Shipper-Account'),
    ('Other-Account-Type', 'Other-Account-Type'),
    
]

class NaqelUser(AbstractUser):
    objects = UserManager()
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_(
        "Enter a valid international mobile phone number starting with +(country code)"))
    mobile_phone = models.CharField(validators=[phone_regex], verbose_name=_(
        "Mobile phone"), max_length=20, unique=True, null=True)
    username = models.CharField(
        'username', max_length=50, unique=True, db_index=True)
        
    fullname = models.CharField(
        'fullname', max_length=191, null=True, blank=True)
    email = models.EmailField(max_length=191, unique=True)
    additional_information = models.CharField(verbose_name=_(
        "Additional information"), max_length=100, blank=True, null=True)
    created_date = models.DateTimeField(default=now, blank=True)
    firebaseuid = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    firebasedeviceid = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return f"{self.username}: {self.email}:{self.fullname} "

class status(models.Model):
    code=models.CharField(max_length=100, null=True, blank=True)
    name=models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return f"{self.code}: {self.name} "

class country(models.Model):
    code=models.CharField(max_length=100, null=True, blank=True)
    name=models.CharField(max_length=100, null=True, blank=True)
    info_Country_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} "

class city(models.Model):
    code=models.CharField(max_length=100, null=True, blank=True)
    name=models.CharField(max_length=100, null=True, blank=True)
    station = models.CharField(max_length=100, null=True, blank=True)
    country = models.ForeignKey(country, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return f"{self.name} "



class state(models.Model):
    code=models.CharField(max_length=100, null=True, blank=True)
    name=models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return f"{self.code}: {self.name} "

class podtype(models.Model):
    code=models.CharField(max_length=100, null=True, blank=True)
    name=models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return f"{self.code}: {self.name} "

class shipmenttype(models.Model):
    code=models.CharField(max_length=100, null=True, blank=True)
    name=models.CharField(max_length=100, null=True, blank=True)
    type=models.CharField(max_length=100, null=True, blank=True)
    shipment_id=models.IntegerField(null=True, blank=True)
    ServiceTypeID=models.IntegerField(null=True, blank=True)
    ServiceType=models.CharField(max_length=100, null=True, blank=True)
    ClientID=models.CharField(max_length=100, null=True, blank=True)
    infotrack_id = models.IntegerField(null=True, blank=True)    

    def __str__(self):
        return f"{self.name}"

class billingtype(models.Model): 
    code=models.CharField(max_length=100, null=True, blank=True)
    name=models.CharField(max_length=100, null=True, blank=True)
    type=models.CharField(max_length=100, null=True, blank=True)    

    def __str__(self):
        return f"{self.name}"        


class CompanyProfile(models.Model):
    company_name=models.CharField(max_length=100, null=True, blank=True)
    client_id = models.CharField(
        max_length=100, unique=True, null=True, blank=True)
    registration_number=models.CharField(max_length=100,null=True, blank=True)
    phone_number=models.CharField(max_length=100, null=True, blank=True)
    email_address=models.CharField(max_length=100, null=True, blank=True)
    country= models.ForeignKey("country",related_name="company_country", on_delete=models.SET_NULL,null=True, blank=True)
    city=models.ForeignKey("city",related_name="comapny_city", on_delete=models.SET_NULL,null=True, blank=True)
    state=models.ForeignKey("state",related_name="company_state", on_delete=models.SET_NULL,null=True, blank=True)
    post_code=models.IntegerField(null=True, blank=True)
    comapny_origin=models.ForeignKey("city",related_name="company_org_city", on_delete=models.SET_NULL,null=True, blank=True)
    location = models.CharField(max_length=100,null=True, blank=True)
    allowed_users=models.ManyToManyField("NaqelUser",null=True, blank=True)
    customer_type = models.CharField(max_length=100,null=True, blank=True)

    def __str__(self):
        return f"{self.company_name} " 
    

class address(models.Model):
    contact_person = models.CharField(max_length=100, null=True, blank=True)
    address1 = models.CharField(max_length=100, null=True, blank=True)
    address2 = models.CharField(
        max_length=100, null=True, blank=True)
    mobile_number1 = models.CharField(max_length=100, null=True, blank=True)
    mobile_number2 = models.CharField(max_length=100, null=True, blank=True)
    country = models.ForeignKey("country",related_name="address_country", on_delete=models.SET_NULL,null=True, blank=True)
    city = models.ForeignKey("city",related_name="address_city", on_delete=models.SET_NULL,null=True, blank=True)
    client = models.ForeignKey("client",related_name="shipper_client", on_delete=models.SET_NULL,null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lng = models.FloatField(null=True, blank=True)
    

    

    def __str__(self):
        return f"{self.address1} " 

#Added for New Booking Screen

class consignee(models.Model):
    company_name = models.ForeignKey("CompanyProfile",related_name="consignee_comapny_name", on_delete=models.SET_NULL,null=True, blank=True)
    contact_person=models.CharField(max_length=100, null=True, blank=True)
    contact_number =  models.CharField(max_length=100, null=True, blank=True)
    mobile_number =  models.CharField(max_length=100, null=True, blank=True)
    address=  models.CharField(max_length=191, null=True, blank=True) 
    country = models.ForeignKey("country",related_name="consignee_country", on_delete=models.SET_NULL,null=True, blank=True)
    city = models.ForeignKey("city",related_name="consignee_city", on_delete=models.SET_NULL,null=True, blank=True)
    pickup_point =  models.CharField(max_length=100, null=True, blank=True)
    shipping_instruction =  models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=70, blank=True, null=True)
    zip_code=models.IntegerField(null=True, blank=True)
    
    @classmethod
    def create(cls,request,company_name,contact_person,contact_number,mobile_number,address,country,city,pickup_point,email,zip_code):
        cons=cls(company_name,contact_person,contact_number,mobile_number,address,country,city,pickup_point,email,zip_code) 
        return cons
# class consignee(models.Model):
#     contact_person1 = models.ForeignKey("consignee",related_name="consignee_contact_person", on_delete=models.SET_NULL,null=True, blank=True)
#     contact_person = models.CharField(max_length=100, null=True, blank=True)
#     address1 = models.CharField(max_length=100, null=True, blank=True)
#     address2 = models.CharField(
#         max_length=100, null=True, blank=True)
#     mobile_number1 = models.CharField(max_length=100, null=True, blank=True)
#     mobile_number2 = models.CharField(max_length=100, null=True, blank=True)
#     email_id=models.CharField(max_length=100, null=True, blank=True)
#     country = models.ForeignKey("country",related_name="consignee_country", on_delete=models.SET_NULL,null=True, blank=True)
#     city = models.ForeignKey("city",related_name="consignee_city", on_delete=models.SET_NULL,null=True, blank=True)
#     client = models.ForeignKey("client",related_name="consignee_client", on_delete=models.SET_NULL,null=True, blank=True)
#     lat = models.FloatField(null=True, blank=True)
#     lng = models.FloatField(null=True, blank=True)
#     is_inactive= models.BooleanField(default=False)
    
#     def __str__(self):
#         return f"{self.contact_person} "
        
#     def __unicode__(self):
#         return self.contact_person        

# class Booking(models.Model):
#     reference = models.CharField(max_length=100, null=True, blank=True)
#     company_name = models.ForeignKey("CompanyProfile",related_name="booking_comapny_name", on_delete=models.SET_NULL,null=True, blank=True)
#     shipper=models.ForeignKey("shipper",related_name="shipper_booking", on_delete=models.SET_NULL,null=True, blank=True)
#     consignee=models.ForeignKey("consignee",related_name="consignee_booking", on_delete=models.SET_NULL,null=True, blank=True)
#     service_type=models.ForeignKey("standardcode",related_name="service_type", on_delete=models.SET_NULL,null=True, blank=True)
#     gross_weight=models.FloatField(null=True, blank=True)
#     piece_count=models.IntegerField(null=True, blank=True)
#     additonal_services=models.CharField(max_length=100, null=True, blank=True)
#     chargable_weight=models.FloatField(null=True, blank=True)
#     customs_value=models.FloatField(null=True, blank=True)
#     goods_origin=models.CharField(max_length=100, null=True, blank=True) 
#     remarks=models.CharField(max_length=100, null=True, blank=True)
#     booking_date=models.DateField(max_length=10, verbose_name="booking_Pickup_Date",null=True, blank=True)      
#     ready_time=   models.TimeField(("Booking_Ready_Time"), null=True, blank=True)          
#     Latest_time= models.TimeField(("Booking_Latest_time"), null=True, blank=True)
#     payment_method=models.CharField(verbose_name=u"payment method",
#                                   max_length=50,
#                                   choices=PAYMENT_METHOD,
#                                   default='Cash', null=True, blank=True)




#     bookingref = models.CharField( max_length=8, blank=True, null=True, verbose_name=_(u'Booking#'))
#     company_profile=models.ForeignKey(CompanyProfile,verbose_name="Company", on_delete=models.SET_NULL,null=True, blank=True)
#     pickup_date = models.DateField(max_length=10, verbose_name="Pickup_Date",null=True, blank=True)
#     pickup_time = models.TimeField(("Booking_Pickup_time"), null=True, blank=True)
#     booking_status= models.CharField(verbose_name=u"Booking Status",
#                                   max_length=25,
#                                   choices=BOOKING_STATUS,
#                                   default='Booked', null=True, blank=True)
#     is_SMS = models.BooleanField(default=False,null=True, blank=True)
#     is_Push = models.BooleanField(default=False,null=True, blank=True)    
#     is_Email =models.BooleanField(default=False,null=True, blank=True)
#     is_fav =models.BooleanField(default=False,null=True, blank=True)
#     pickup_point = models.CharField(max_length=191, null=True, blank=True)                                                
    
#     def save(self, *args, **kwargs):
#         if self.__class__.objects.all().count() == 0:
#             letter =  "BK"
#             number = 1
#             self.bookingref ="{0}{1:0>2d}".format(letter,number)   # 'A001' this time
#         else:
#             last_id = self.__class__.objects.all().order_by("-id")[0].id + 1
#             letter =  "BK"
#             number = (last_id+1)
#             self.bookingref = "{0}{1:0>2d}".format(letter,number)
#         super(self.__class__, self).save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.company_profile} "


class WaybillGenerate(models.Model):
    LatestWaybillNo = models.CharField(max_length=20,primary_key=True, blank=True)

#Added for New Booking Screen
class shipper(models.Model):
    company_profile = models.ForeignKey("CompanyProfile",related_name="shipper_comapny_name", on_delete=models.SET_NULL,null=True, blank=True)
    contact_person=models.CharField(max_length=100, null=True, blank=True)
    company_name=models.CharField(max_length=100, null=True, blank=True)
    contact_number =  models.CharField(max_length=100, null=True, blank=True)
    mobile_number =  models.CharField(max_length=100, null=True, blank=True)
    address=  models.CharField(max_length=191, null=True, blank=True) 
    country = models.ForeignKey("country",related_name="shipper_country", on_delete=models.SET_NULL,null=True, blank=True)
    city = models.ForeignKey("city",related_name="shipper_city", on_delete=models.SET_NULL,null=True, blank=True)
    pickup_point =  models.CharField(max_length=100, null=True, blank=True)
    shipping_instruction =  models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(max_length=100, null=True, blank=True)
    is_default = models.BooleanField(verbose_name=_(
        "is_default"), default=1, blank=True, null=True)
    

class client(models.Model):
    company_name = models.CharField(max_length=100, null=True, blank=True)
    account_number = models.CharField(
        max_length=100, unique=True, null=True, blank=True)
    mobile_number = models.CharField(max_length=100, null=True, blank=True)
    country = models.ForeignKey("country", on_delete=models.SET_NULL,null=True, blank=True)
    city = models.ForeignKey("city",related_name="client_city", on_delete=models.SET_NULL,null=True, blank=True)

    def __str__(self):
        return f"{self.company_name} " 
       


 

class Tracking(models.Model):
    waybillno = models.IntegerField(unique=True, db_index=True)
    reference = models.CharField(max_length=100, blank=True, null=True)
    pickupdate = models.DateTimeField(default=now, blank=True)
    currentstatus = models.CharField(max_length=191, blank=True, null=True)
    destination = models.CharField(max_length=100, blank=True, null=True)
    currentstatusar = models.CharField(max_length=191, blank=True, null=True)
    destinationar = models.CharField(max_length=100, blank=True, null=True)
    piececount = models.IntegerField(blank=True, null=True)
    expected_delivery = models.DateTimeField(
        default=now, blank=True)
    paymentmethod = models.CharField(max_length=100, blank=True, null=True)
    iscompleted = models.BooleanField(blank=True, null=True)
    mobile_phone = models.CharField(verbose_name=_(
        "Mobile phone"), max_length=17, blank=True, null=True)
    email = models.EmailField(max_length=70, blank=True, null=True)
    is_sync = models.BooleanField(verbose_name=_(
        "is_sync"), default=False, blank=True, null=True)
    eventCode = models.IntegerField(blank=True, null=True)

class TrackingDetails(models.Model):
    refrenceid = models.IntegerField(unique=True, db_index=True)
    waybillno = models.ForeignKey(
        Tracking, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=191, blank=True, null=True)
    descriptionAr = models.CharField(max_length=191, blank=True, null=True)
    statusid = models.IntegerField(blank=True, null=True)
    actiondate = models.DateTimeField(default=now, blank=True)
    actiontime = models.TimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True)
    location = models.CharField(max_length=191, blank=True, null=True)
    locationAr = models.CharField(max_length=191, blank=True, null=True)
    isdeleted = models.BooleanField(blank=True, null=True)
    employid = models.IntegerField(blank=True, null=True)
    is_sync = models.BooleanField(verbose_name=_(
        "is_sync"), default=False, blank=True, null=True)
    eventCode = models.IntegerField(blank=True, null=True)


class SystemVariables (models.Model):
    variableKey = models.CharField( max_length=191, null = True,blank=True, db_index=True)
    
    variableValue = models.CharField( max_length=100,null = True,blank=True, db_index=True)

    def __str__(self):
        return str(self.variableValue)


class SchedulingReason (models.Model):
    Name =models.CharField(max_length=100, verbose_name="Reason",null=True)
    StatusID=models.IntegerField(verbose_name="StatusID",null=True)
    def __str__(self):
        return f"{self.Name} "


class IndustryType (models.Model):
    Type=models.CharField(max_length=100, verbose_name="IndustType",null=True)

    def __str__(self):
        return f"{self.Type} "
 
class B2BRegisteration(models.Model):
    ComName=models.CharField(max_length=100, verbose_name="CompanyName")
    CustomerName =models.CharField(max_length=100, verbose_name="CustomerName")
    IndType=models.ForeignKey(IndustryType,related_name="Ind_type", on_delete=models.CASCADE,null=True, blank=True)
    MoNumber =models.CharField(max_length=50, verbose_name="MobileNo")
    Email = models.EmailField(max_length=191, blank=True, null=True)
    Address = models.CharField(max_length=100, verbose_name="Address")
    city=models.ForeignKey(city,related_name="com_city", on_delete=models.CASCADE,null=True, blank=True)
    country= models.ForeignKey(country,related_name="Comp_country", on_delete=models.CASCADE,null=True, blank=True)
    def __str__(self):
        return f"{self.ComName} "
class BarcodeCount(models.Model):
    waybillno = models.ForeignKey("Booking",related_name="barcode_waybill", on_delete=models.SET_NULL,null=True, blank=True)
    barcode_number =models.CharField(max_length=100, null=True, blank=True)
    
class EnquiryModule(models.Model):
    Name=models.CharField(max_length=100, verbose_name="EName")
    Email = models.EmailField(
        max_length=191, blank=False, null=False)
    PhoneNo=models.CharField(max_length=100, verbose_name="PhoneNumber")
    Details=models.CharField(max_length=191, verbose_name="Details")
    def __str__(self):
        return f"{self.Name} "

class ComplaintsType (models.Model):
    Type=models.CharField(max_length=100, verbose_name="CAFType",null=True)
    def __str__(self):
        return f"{self.Type} "
class ComplaintsModule(models.Model):
    Name=models.CharField(max_length=100, verbose_name="EName")
    Email = models.EmailField(
        max_length=191, blank=False, null=False)
    PhoneNo=models.CharField(max_length=100, verbose_name="PhoneNumber")
    Reason =models.ForeignKey(ComplaintsType,related_name="CAF_Type", on_delete=models.CASCADE,null=True, blank=True)
    Details=models.CharField(max_length=191, verbose_name="Details")
    evidence=models.FileField(upload_to='CAFevidence/',blank=True,null=True)
    def __str__(self):
        return f"{self.Name} "

class CScontact(models.Model):
    account_number=models.ForeignKey(client,related_name="account", on_delete=models.CASCADE,null=True, blank=True)
    CsEmail=models.EmailField(
        max_length=191, blank=False, null=False)
    CSContactNo=models.CharField(max_length=100, verbose_name="CSContactNo")

class KeyAccountContact(models.Model):
    account_number=models.ForeignKey(client,related_name="accountNo", on_delete=models.CASCADE,null=True, blank=True)
    KeyEmail=models.EmailField(
        max_length=191, blank=False, null=False)
    KeyContactNo=models.CharField(max_length=100, verbose_name="KeyContactNo")
  

class UploadStaging (models.Model):
    refno =models.CharField(max_length=191, null=True, blank=True) 
    origin =models.CharField(max_length=191, null=True, blank=True) 
    Destination =models.CharField(max_length=191, null=True, blank=True) 
    Name =models.CharField(max_length=191, null=True, blank=True) 
    Email =models.CharField(max_length=191, null=True, blank=True) 
    PhoneNo =models.CharField(max_length=191, null=True, blank=True) 
    MobileNo =models.CharField(max_length=191, null=True, blank=True) 
    Address =models.CharField(max_length=191, null=True, blank=True) 
    Location =models.CharField(max_length=191, null=True, blank=True) 
    POBox =models.CharField(max_length=191, null=True, blank=True) 
    Date =models.DateField(max_length=10, verbose_name="Pickup Date",null=True, blank=True)
    Peices =models.IntegerField(verbose_name="pcs",null=True, blank=True)
    Weight =models.FloatField(null=True, blank=True)
    Width =models.FloatField(null=True, blank=True)
    Length =models.FloatField(null=True, blank=True)
    Height =models.FloatField(null=True, blank=True)
    CODAmount =models.FloatField(null=True, blank=True)
    DeliveryInstruction =models.CharField(max_length=191, null=True, blank=True) 
    PODType =models.CharField(max_length=191, null=True, blank=True) 
    DeclaredValue =models.FloatField( null=True, blank=True) 
    GoodDesc =models.CharField(max_length=191, null=True, blank=True) 
    ConsigneeNationalID =models.CharField(max_length=191, null=True, blank=True) 
    GoodDesc =models.CharField(max_length=191, null=True, blank=True) 
    message =models.CharField(max_length=191, null=True, blank=True) 
    sessionUserID=models.CharField(max_length=191, null=True, blank=True)

class StandardCode (models.Model):
    CodeType =models.CharField(max_length=50, null=True, blank=True) 
    CodeValue =models.CharField(max_length=191, null=True, blank=True) 
    RefID =models.CharField(max_length=50, null=True, blank=True) 

    def __str__(self):
        return f"{self.CodeValue}" 
   










