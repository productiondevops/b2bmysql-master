from django.contrib import admin
from core.models import *
from core.forms import *
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
@admin.register(city)
class CityAdmin(ImportExportModelAdmin):
    pass


@admin.register(shipmenttype)
class ShipmenTypeAdmin(ImportExportModelAdmin):
    pass

class NaqelUserAdmin(UserAdmin):
     search_fields = ['username', 'mobile_phone', 'email', ]
     list_display = ('id','username', 'mobile_phone', 'email', )
 
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name','client_id','registration_number','phone_number','email_address','country','city','state','post_code',)
admin.site.register(CompanyProfile, CompanyProfileAdmin)
 
# class BookingAdmin(admin.ModelAdmin):
#     list_display = ('id','company_profile', 'pickup_date','pickup_time','booking_status',)
# admin.site.register(Booking, BookingAdmin)


class ConsigneeAdmin(admin.ModelAdmin):
    list_display = ('company_name','contact_person','contact_number',
                    'mobile_number','address','country','city','pickup_point','shipping_instruction','account_number')
admin.site.register(consignee, ConsigneeAdmin)


class ShipperAdmin(admin.ModelAdmin):
    list_display = ('company_name','contact_person','contact_number',
                    'mobile_number','address','country','city','pickup_point','shipping_instruction','account_number')
admin.site.register(shipper, ShipperAdmin)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('company_name','account_number','mobile_number','country','city',)
admin.site.register(client, ClientAdmin)

class AddressAdmin(admin.ModelAdmin):
    list_display = ('contact_person','address1','address2','mobile_number1','mobile_number2','country','city','client','lat','lng',)
admin.site.register(address, AddressAdmin)


# class CityAdmin(admin.ModelAdmin):
#     list_display = ('code','name',)
# admin.site.register(city, CityAdmin)

@admin.register(country)
class CountryAdmin(ImportExportModelAdmin):
    pass

class StateAdmin(admin.ModelAdmin):
    list_display = ('code','name',)
admin.site.register(state, StateAdmin) 

class PodtypeAdmin(admin.ModelAdmin):
    list_display = ('code','name',)
admin.site.register(podtype, PodtypeAdmin)

# class ShipmenTypeAdmin(admin.ModelAdmin):
#     list_display = ('code','name','type')
# admin.site.register(shipmenttype, ShipmenTypeAdmin)

class billingtypeAdmin(admin.ModelAdmin):
    list_display = ('code','name','type')
admin.site.register(billingtype, billingtypeAdmin)

class EstimatedDeliveryDurationAdmin(admin.ModelAdmin):

    list_display = ('date', 'time', 'originCountry',
                    'originCity', 'destinationCountry', 'destinationCity', 'serviceType', 'productType','weight','createdDate')


#admin.site.register(EstimatedDeliveryDuration, EstimatedDeliveryDurationAdmin)
admin.site.register(NaqelUser,NaqelUserAdmin)

class B2BRegisterationAdmin(admin.ModelAdmin):
     list_display =('ComName', 'CustomerName','IndType','MoNumber','Address','city','country')

admin.site.register(B2BRegisteration)

class IndustryTypeAdmin(admin.ModelAdmin):
     list_display =('Type')

admin.site.register(IndustryType)

class ComplaintsTypeAdmin(admin.ModelAdmin):
     list_display =('Type')

admin.site.register(ComplaintsType)

class ComplaintsModuleAdmin(admin.ModelAdmin):
     list_display =('Name', 'Email', 'PhoneNo','Reason','Details','evidence')

admin.site.register(ComplaintsModule)

class EnquiryModuleAdmin(admin.ModelAdmin):
     list_display =('Name', 'Email','PhoneNo','Details')

admin.site.register(EnquiryModule)


class CScontactAdmin(admin.ModelAdmin):
     list_display =('account_number', 'CsEmail', 'CSContactNo')

admin.site.register(CScontact)


class KeyAccountContactAdmin(admin.ModelAdmin):
     list_display =('account_number', 'KeyEmail', 'KeyContactNo')

admin.site.register(KeyAccountContact)

class SchedulingReasonAdmin(admin.ModelAdmin):
     list_display =('Name','StatusID')

admin.site.register(SchedulingReason)




class StandardCodeAdmin(admin.ModelAdmin):
    list_display = ('CodeType','CodeValue','RefID')
admin.site.register(StandardCode, StandardCodeAdmin)




