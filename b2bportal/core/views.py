#Email pass

from email import message
from urllib.request import Request
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetConfirmView,PasswordContextMixin
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages #import messages
from django.utils.html import format_html
#Email
from .booking import CustomerWaybill,ShipmentBookingForm
from dataclasses import field, fields
from email.policy import default
from msilib.schema import Class
#from msilib.schema import tables
from multiprocessing import context
from telnetlib import STATUS
from types import CodeType
from urllib import response
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render
from requests import request
from django.template.loader import get_template
from xhtml2pdf import pisa

#pdf generate
import reportlab
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

#pdf generate
from .forms import *
from django.template.response import TemplateResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import logging
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager
 
import django_tables2 as tables
from django.core.management import call_command
from django.views.decorators.http import require_http_methods, require_GET
# Create your views here.
from decimal import Decimal
from django.db.models import Q
import django_filters
from django_tables2 import SingleTableMixin, TemplateColumn
from django_filters.views import FilterView
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import views as auth_views
from django.db.models import Prefetch
from django.db.models import Count
from django.db import transaction
from sequences import Sequence
from django.db.models.signals import post_save
from django.dispatch import receiver

WaybillNumber = Sequence("waybill_numbers",initial_value=235255555)
document_no = Sequence("doc_numbers",initial_value=1000)
#for tracking : import below
from ast import Or, arg
from django.shortcuts import render
from datetime import datetime
import re
import requests
from requests.api import patch
from .forms import  *
import time as tt
#tracking end
from django.contrib.staticfiles import finders
from django.conf import settings
import os
from core.EmailUtility import send_html_mail
from django.http import HttpResponseRedirect
from tablib import Dataset

from .config import BaseConfig as CC
import json
from .services import pbiembedservice as PbiEmbedService
from django.http import HttpResponse
# import pywhatkit as kit

import mimetypes

api_host="http://212.107.118.74:81/b2b/"
# from django.contrib.sites.shortcuts import get_current_site
 
 
def get_embed_info(request):
    try:

        B2B="21c9a08b-2d55-46af-97a7-19bd5977092b"
        B2C="3da14145-f206-4ed0-b254-8a05bc0b6145"
        POWERBI_ID="21c9a08b-2d55-46af-97a7-19bd5977092b"
        company=GetCurrentCompany(request)
        cust_type=company.customer_type
        if cust_type == 'B2B':
            POWERBI_ID=B2B
        else:
            POWERBI_ID=B2C
            
        pb= PbiEmbedService.PbiEmbedService()
        embed_info = pb.get_embed_params_for_single_report(CC.WORKSPACE_ID, POWERBI_ID)
        return HttpResponse(embed_info, content_type='application/json')
    except Exception as ex:
        return json.dumps({'errorMsg': str(ex)}), 500

 
def Price_Estimator(request):
    print("Rashmi")
    if request.htmx:
            base_template="b2bportal/_partial.html"
    else:
        base_template="b2bportal/base.html"
        
    url ="https://infotrack.naqelexpress.com/NaqelAPIServices/NaqelAPI/9.0/XMLShippingService.asmx?op=GetRate"
    print(url)
    payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:GetRate>
         <!--Optional:-->
         <tem:ClientInfo>
            <!--Optional:-->
            <tem:ClientAddress>
               <!--Optional:-->
               <tem:PhoneNumber>0532155580</tem:PhoneNumber>
               <!--Optional:-->
               <tem:POBox>Box</tem:POBox>
               <!--Optional:-->
               <tem:ZipCode>1002</tem:ZipCode>
               <!--Optional:-->
               <tem:Fax>?</tem:Fax>
               <!--Optional:-->
               <tem:FirstAddress>?</tem:FirstAddress>
               <!--Optional:-->
               <tem:Location>?</tem:Location>
               <!--Optional:-->
               <tem:CountryCode>1</tem:CountryCode>
               <!--Optional:-->
               <tem:CityCode>1</tem:CityCode>
            </tem:ClientAddress>
            <!--Optional:-->
            <tem:ClientContact>
               <!--Optional:-->
               <tem:Name>?</tem:Name>
               <!--Optional:-->
               <tem:Email>?</tem:Email>
               <!--Optional:-->
               <tem:PhoneNumber>?</tem:PhoneNumber>
               <!--Optional:-->
               <tem:MobileNo>?</tem:MobileNo>
            </tem:ClientContact>
            <tem:ClientID>9020077</tem:ClientID>
            <!--Optional:-->
            <tem:Password>test1234</tem:Password>
            <!--Optional:-->
            <tem:Version>9.0</tem:Version>
         </tem:ClientInfo>
         <tem:Weight>5</tem:Weight>
         <tem:LoadTypeID>39</tem:LoadTypeID>
         <tem:FromDate>2022-10-26</tem:FromDate>
         <!--Optional:-->
         <tem:Origin>DMM</tem:Origin>
         <!--Optional:-->
         <tem:Destination>RUH</tem:Destination>
      </tem:GetRate>
   </soapenv:Body>
</soapenv:Envelope>
"""
    
    headers = {
        'Content-Type': 'text/xml; charset=utf-8'
    }
    response = requests.request("POST", url, headers=headers, data=payload)  
    records=response.content
    print(records)
     
    form=RateCalForm(request.POST)
    context={
         'form':form,
         'base_template':base_template
    }
    return render(request, 'b2bportal/Price_Estimator.html',context =context)
 
def GetCurrentCompany(request):
    company=None
    for comp in CompanyProfile.objects.all():
        data = comp.allowed_users.all().filter(id=request.user.id)
        if data:
            company = comp
            break
    return company
  

def success(request):
   showsummary=Booking.objects.all()
   context={
        'showsummary':showsummary
   }
   return render(request, 'b2bportal/success.html',context)
 


def pdf_report_create(request):
    showsummary=Booking.objects.all()
    template_path = 'b2bportal/pdfreport.html'
    context = {
        'showsummary':showsummary
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    showsummary=Booking.objects.all()
    return response    

    
@login_required(login_url="/premium-login")
def dashboard(request):   
    context={}
    data=[]
    company=GetCurrentCompany(request)
    # ClientID=company.client_id
    ClientID=9019614
    service_list=StandardCode.objects.filter(CodeType='ServiceType')
    product_list=StandardCode.objects.filter(CodeType='ProductType')
    Region_list=StandardCode.objects.filter(CodeType='RegionType')
    city_list=city.objects.filter(code='CityCode')
    
    context={
        "standardcode":service_list, 
        "productCode":product_list,
        "RegionCode":Region_list,                                                           
        "CityCode":city_list,
    }
    if request.htmx:
        base_template="b2bportal/_partial.html"
    else:
        base_template="b2bportal/base.html"
 
    if "ServiceTypeID" in request.GET:
        request.session["ServiceTypeID"]=request.GET["ServiceTypeID"]
    if "ProductTypeID" in request.GET:
        request.session["ProductTypeID"]=request.GET["ProductTypeID"]

    if "RegionID" in request.GET:
        request.session["RegionID"]=request.GET["RegionID"]        
    
    ProductTypeID=request.session.get("ProductTypeID",7)
    ServiceTypeID=request.session.get("ServiceTypeID",2)
    RegionID=request.session.get("RegionID",3)
    CityID=3

 
    if request.method == 'POST':
        print('post')
        form = DashboardForm(request.POST)
         
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        
        request.session["from_date"]=str(from_date)
        request.session["to_date"]=str(to_date)
 
 
        data=None
        context={}
        form = DashboardForm(
            initial={"from_date":from_date,"to_date":to_date}
        )
        
        context["base_template"]=base_template
       
        return render(request, 'b2bportal/dashboard.html',context=context)
     
    else:
        print('get')
        

        
        
        context["base_template"]=base_template
        return render(request, 'b2bportal/dashboard.html', context=context)
class BookingHTMxTable(tables.Table):


    actions = TemplateColumn(template_code="""
    
    {% if record.booking_no.booking_status == "Cancel-Booking" %} &nbsp;
    {% else %}
    <ul class="navbar-nav">
                <li class="nav-item  dropdown">
                <a class="nav-link dropdown-toggle" href="http://example.com" id="navbarDropdownMenuLink" data-toggle="dropdown">
               
                </a>
                <div class="dropdown-menu dropdown-menu-right" aria-labelledby="navbarDropdownMenuLink">
                    
                  
                  <a class="dropdown-item" style="color: red;{% if record.booking_no.booking_status == "Picked-Up" %} display:None;{%endif%}"   hx-get="{% url 'home:deletebooking' record.booking_no.pk %}" hx-confirm="Are you sure you want to delete this customer?" hx-target="#dialog" href="{% url 'home:deletebooking' record.booking_no.pk %}" ><i class="fa fa-trash fa-2x mr-2"></i> Delete</a>
                  <a class="dropdown-item" style="color: blue;{% if record.booking_no.booking_status == "Picked-Up" %} display:None;{%endif%}"  hx-get="/reschedulebooking/{{record.booking_no.pk}}" hx-target="#dialog" href="/reschedulebooking/{{record.booking_no.pk}}"><i class="fa fa-calendar  fa-2x mr-2 mr-2"></i>Reshedule</h5></a>
                  <a class="dropdown-item" style="color: blue;"  href="/SuccessView/{{record.booking_no.id}}"><i class="fa fa-eye fa-2x mr-2"></i>View</h5></a>
                </div>
              </li>
      </ul>
     {% endif %}
""")

    notify= TemplateColumn(template_code="""
 

    <ul class="navbar-nav">
                <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="http://example.com" id="navbarDropdownMenuLink" data-toggle="dropdown">
                <i class="nc-icon nc-bell-55"></i>
                </a>
                <div class="dropdown-menu dropdown-menu-left" aria-labelledby="navbarDropdownMenuLink">
                
                  <a class="dropdown-item" style="color: blue;"   hx-get="{% url 'home:alertnotification' record.booking_no.pk 2 %}" hx_swap="innerHTML" href="{% url 'home:alertnotification' record.booking_no.pk 2 %}">
                  {%if record.booking_no.is_Push == True %}<i class='fa fa-check mr-2 mr-2'></i>{% endif %}
                  Push</h5></a>
                  <a class="dropdown-item" style="color: blue;"  hx-get="{% url 'home:alertnotification' record.booking_no.pk 3 %}" hx_swap="innerHTML" href="{% url 'home:alertnotification' record.booking_no.pk 3 %}">
                  {%if record.booking_no.is_Email == True %}<i class='fa fa-check mr-2 mr-2'></i>{% endif %}
                  Email</h5></a>
                </div>
              </li>
      </ul>
""")
    check= TemplateColumn(template_code=""" 
    <input name="selectaction" value={{record.pk}} type="checkbox" style="opacity:10;"></input> 

""")

    class Meta:
        model = CustomerWaybill
        template_name = "b2bportal/common/bootstrap_htmx.html"
        fields = ['check','notify','waybillno','booking_no__bookingref','booking_no__company_profile','origin_city', 'destination_city',
                  'booking_no__booking_status','booking_no__pickup_date', 'weight', 'shipment_type', 'actions']
  
class BookingFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='booking_no__pickup_date',
                                           widget= forms.DateInput(attrs={'class': 'form-control dateheight', 'type': 'date',}  ),
                                         label='',method='universal_search')
                                        
    end_date = django_filters.DateFilter(field_name='booking_no__pickup_date',
                                         widget= forms.DateInput(attrs={'class': 'form-control dateheight', 'type': 'date'}),
                                          label='',method='universal_search')

    query = django_filters.CharFilter(method='universal_search1', label="", widget=forms.TextInput(attrs={'class': 'form-control ml-5 dateheight','placeholder': 'Filter(waybill,org,dest,status,Type)',}))
    #query = django_filters.CharFilter(field_name='booking_no__booking_status', label="", widget=forms.TextInput(attrs={'class': 'form-control ml-5','placeholder': 'Filter(waybill,org,dest,status,Type)',}))

    def __init__(self, *args, **kwargs):
        super(BookingFilter, self).__init__(*args, **kwargs)
        self.form.initial['start_date'] = date.today
        self.form.initial['end_date'] = date.today
       
    class Meta:
        model = CustomerWaybill
        fields = ['start_date','end_date']

    def universal_search(self, queryset, booking_no, value):
        start_date=self.request.GET.get("start_date",None)
        end_date=self.request.GET.get("end_date",None)
        query=self.request.GET.get("query",None)
        if query is None:
            print('query none')
            query="pickup"
        print(start_date,end_date,query)
       
        #qs= CustomerWaybill.objects.filter(booking_no__pickup_date__gte=start_date,booking_no__pickup_date__lte =end_date,booking_no__booking_status=query).order_by("-booking_no__pickup_date")
        #print(qs)
        qs= CustomerWaybill.objects.filter(booking_no__pickup_date__gte=start_date,booking_no__pickup_date__lte =end_date)
       
        return qs
    def universal_search1(self, queryset, booking_no, value):
        start_date=self.request.GET.get("start_date",None)
        end_date=self.request.GET.get("end_date",None)
        query=self.request.GET.get("query",None)
        if query is None:
            print('query none')
            query="pickup"
        print(start_date,end_date,query)
       
        #qs= CustomerWaybill.objects.filter(booking_no__pickup_date__gte=start_date,booking_no__pickup_date__lte =end_date,booking_no__booking_status=query).order_by("-booking_no__pickup_date")
        #print(qs)
        return CustomerWaybill.objects.filter(Q(waybillno=value) | Q(origin_city__name=value) | Q(booking_no__bookingref=value) )
        
        return qs

    # def get_queryset(self):
    #     start_date=self.request.GET.get("start_date",None)
    #     end_date=self.request.GET.get("end_date",None)
    #     qs= CustomerWaybill.objects.filter(booking_no__pickup_date__gte=start_date,booking_no__pickup_date__lte =end_date).order_by("-pickup_date")
    #     print('Rashmi queryset1')
    #     return super().get_queryset()

        

class bookingHTMxTableView(SingleTableMixin, FilterView):
    table_class = BookingHTMxTable
    filterset_class = BookingFilter
    
    paginate_by = 6
    #print(filterset_class)
    # CustomerWaybill = BookingFilter(request.GET, queryset=querySet )
  
    def get_queryset(self):
        self.queryset= CustomerWaybill.objects.filter(booking_no__company_profile=GetCurrentCompany(self.request),booking_no__pickup_date__gte=date.today().isoformat(),booking_no__pickup_date__lte =date.today().isoformat()
        ).order_by("-pickup_date")
        print('Rashmi queryset')
        return super().get_queryset()
       
    
    def get_action(self):
        bookingstatus=self.get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_shipments=self.get_queryset()
        under_process=all_shipments.count()
        submitted=all_shipments.filter(booking_no=1).count()
        un_submitted=CustomerWaybill.objects.count()
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
            print('Nouf')
            template_name = "b2bportal/booking_table_partial.html"
        else:
            print('here')
            template_name = "b2bportal/booking.html"
        
        return template_name



def PrintBooking(request):
    template_name=""
    filename=""
    context={

    }
    if request.method == 'POST':
        waybill_ids=request.POST.getlist("selectaction")
        waybill_list=CustomerWaybill.objects.filter(id__in=waybill_ids)
        template_name="WaybillLabelTemplate.ods"
        print('Sticker')
        print(waybill_list)
        if waybill_list.count() > 0 :   
            #print(request.POST)
            myResquet = str(request.POST)
            print(myResquet)
            if myResquet.__contains__("print-sticker-A4"):
                    print ("print-sticker-A4")
                    template_name="WaybillLabelTemplateA5.ods"
                    filename="{0}.pdf".format("print-sticker-A4")
                    
            elif myResquet.__contains__("print-sticker-A5"):
                    print ("print-sticker-A5")
                    filename="{0}.pdf".format("print-sticker-A5")
                    template_name="WaybillLabelTemplate.ods"
                
            elif myResquet.__contains__("print-sticker-label"):
                    print ("print-sticker-label")
                    filename="{0}.pdf".format("print-sticker-label")
                    template_name="WaybillLabelTemplatesticker2.ods"

            context={
                        "data_list":waybill_list
                    }
            return generate_report_document(request,template_name,filename,context)
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



def getconsignee(request, consigneeid):
    print(isinstance(consigneeid, int))
    if consigneeid.isdigit():
        mydata = consignee.objects.get(pk=int(consigneeid))
        print(mydata.contact_person)

    else:
        data = {
            "id": consigneeid,
            "contact_person": consigneeid,
            "country": None,
            "city": None,
            "address1": None,
            "address2": None,
            "mobile_number1": None

        }
        return JsonResponse(data)

    if mydata:
        data = {
            "id": mydata.id,
            "contact_person": mydata.contact_person,
            "country": mydata.country_id,
            "city": mydata.city_id,
            "address1": mydata.address1,
            "address2": mydata.address1,
            "mobile_number1": mydata.mobile_number1

        }
        
        return JsonResponse(data)



def deleteUploadBooking(request):
    print('deleteid',id)
    if request.method == "GET":
        uploadDelete=UploadStaging.objects.filter(pk=id)
        uploadDelete.delete()
        return redirect("/UploadBooking")


def deletebooking(request,id):
    if request.method == "GET":
        wbillno=CustomerWaybill.objects.filter(booking_no_id=id)
        bk=Booking.objects.get(id=id)
        if bk:
            wbillno.delete()
            bk.delete()
            
            html="""
                    <div class="modal-dialog" role="document">
                        <div class="modal-content" sty>
                        <div class="modal-header">
                            <h5 class="modal-title" id="exampleModalLabel"></h5>
                            <button type="button" onclick="javascript:location.reload();" class="close reload" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            <h4> Booking has been deleted !</h4>
                        </div>
                        <div class="modal-footer">
                            <button type="button" onclick="javascript:location.reload();" class="btn btn-secondary reload" data-dismiss="modal">Close</button>
                        </div>
                        </div>
                    </div>
                    
"""
        return HttpResponse(  html )
   
 
     
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
                                    print("Hello")
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
            validdata=records.filter(message="") 
            
            booking=None

           
            for rec in validdata:
                waybill_count=waybill_count+1
                if booking==None: 
                    booking=Booking.objects.create(pickup_point="",pickup_date=datetime.datetime.now(),pickup_time=datetime.datetime.now())
                    booking.company_profile=company
                    booking
                    booking.is_fav=False
                    booking.save()
                
                new_waybill=CustomerWaybill.objects.create()
                new_waybill.company_profile=company
                new_waybill.contact_number = company.phone_number
                new_waybill.contact_number = company.phone_number
                new_waybill.origin_city =city.objects.filter(name= rec.origin).first()
                new_waybill.waybillno=next(WaybillNumber)
                new_waybill.booking_no=booking
                new_waybill.refrenceno=rec.refno
                new_waybill.piece_count=rec.Peices
                new_waybill.weight=rec.Weight
                new_waybill.height=rec.Height
                new_waybill.width=rec.Width
                new_waybill.delivery_instruction=rec.DeliveryInstruction
                new_waybill.pickup_date=datetime.datetime.today()
                #new_waybill.pod_type=rec.PODType
                new_waybill.declare_value=rec.DeclaredValue
                new_waybill.CODAmount=rec.CODAmount
                new_waybill.cust_national_id=rec.ConsigneeNationalID
                
                con = consignee.objects.create()
                con.contact_person = rec.Name
                con.address1 = rec.Address
                con.address2 = "{},{}".format(rec.Location,rec.POBox)
                con.email_id = rec.Email
                con.mobile_number1 = rec.MobileNo
                con.mobile_number2=rec.PhoneNo
                con.is_inactive=True
                con.save()
                
                new_waybill.consignee=con
                new_waybill.destination_city=city.objects.filter(name= rec.Destination).first() 
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
    
    
      

#@receiver(post_save, sender=CustomerWaybill)
#def create_waybill(sender, instance, **kwargs):
#    print('waybill123',instance.pk)
#    bk=Booking.objects.get(pk=instance.pk)
#    for con in bk.consignee_list.all():
#         print('waybillid',con.id)
#         generatewaybill(bk,con)
           


def SuccessView(request,booking_id):
    waybill_list=Booking.objects.filter(booking_no_id=booking_id)
    if waybill_list.count() > 0:
        company=GetCurrentCompany(request)
        booking=waybill_list[0]
        return render(request, 'b2bportal/confirm.html', {
                'booking': booking,
                'waybills': waybill_list,
                'company': company,
            })
    else:
        return HttpResponse(status=204)







# def newbooking(request,booking_id,waybill_id):
#     form=ShipmentBookingForm()
    
#     if request.GET.get('id',None) != None:
#         org_country=request.POST.get("data")
#         city_list=city.objects.filter(country_id=org_country)
#         city_data=""
#         for row in city_list:
#             city_data+="<option value='{}'>{}</option>".format(row.id,row.name)
#         return HttpResponse(city_data)
        
#     bookingref=None
#     waybill=None
#     booking=None

#     print("booking_id",waybill_id)

#     if waybill_id == 0:
       
#         cosigneeFormSet = modelformset_factory(
#             consignee, form=ShipmentBookingForm, extra=1)
#     else:
#         waybill=CustomerWaybill.objects.get(pk=waybill_id)
#         cosigneeFormSet = modelformset_factory(
#         consignee, form=ShipmentBookingForm, extra=0)
    
#     user = NaqelUser.objects.filter(pk=request.user.id)
#     company = None
#     for comp in CompanyProfile.objects.all():
#         data = comp.allowed_users.all().filter(id=request.user.id)
#         if data:
#             company = comp
#             break
     
   
#     if request.method == "POST":
        
        
#         if booking_id > 0 :
#             booking=Booking.objects.get(pk=booking_id)
            

#         form = WaybillForm(request.POST)
#         formset =cosigneeFormSet(request.POST,queryset=consignee.objects.all(), prefix='form2')
#         if form.is_valid():

           
#             form_data = form.save(commit=False)
 
#             # check for existing booking in session otherwise create new booking.
#             if booking==None:
#                 booking=Booking.objects.create(pickup_point=form_data.pickup_point,
#                 pickup_date=form_data.pickup_date,
#                 pickup_time=form_data.pickup_time
#                 )
#                 booking.company_profile=company
#                 if request.POST.get("pintoservice") == "1":
#                    booking.is_fav=True
#                 print('save Rashmi')
#                 booking.save()
                 
#             form_data.contact_number = company.phone_number
#             form_data.origin_city = company.city
#             form_data.destination_city=company.city 
#             form_data.company_profile=company
#             form_data.booking_no=booking
#             form_data.refrenceno=booking.bookingref

           
#             if waybill_id > 0:
#                 form_data.pk=waybill_id
                  
#                 form_data.waybillno=waybill.waybillno
                
#             else:

#                 form_data.waybillno=next(WaybillNumber)
                
#             #form_data.consignee=waybill.consignee
             
#             if formset.is_valid():
#                 formset_data = formset.save(commit=False)
#                 con = None
#                 for f in formset_data:
#                     if f.contact_person.isdigit():
#                         con = consignee.objects.get(pk=int(f.contact_person))
#                         print("Naqel",con)
#                     else:
#                         con = consignee.objects.create()
#                         con.contact_person = f.contact_person
#                         con.save()

#                     con.address1 = f.address1
#                     con.address2 = f.address2
#                     con.country = f.country
#                     con.city = f.city
#                     con.mobile_number1 = f.mobile_number1
#                     con.save()
#                     form_data.consignee=con
#             else:
#                 print("invalid", formset.errors)
            
#             form_data.save()
#             waybill_list=CustomerWaybill.objects.filter(booking_no_id=booking.id)

#             return render(request, 'b2bportal/success.html', {
#             'booking': booking,
#             'waybills': waybill_list,
#             'company': company
#         })
#         else:
#             print("Naqel",form.errors)
#             return HttpResponse(status=204)
     


#         pass
#     else:
#         # Edit old Waybills
 
#         if waybill_id > 0:
            
#             form=WaybillForm(instance=waybill)
#             formset = cosigneeFormSet(queryset=consignee.objects.filter(id=waybill.consignee.id), prefix='form2')
#             print('printing formset if part',formset)

#         else:
#             form = WaybillForm(initial={
#                 'weight': 1.0,
#                 'piece_count': 1,
#                 'pickup_date': strftime('%Y-%m-%d'),
#                 'pickup_time': strftime("%H:%M"),
#                 'height': 1,
#                 'width': 1,
#                 'length': 1,
#                 'vol_weight': '1.0',
#                 'shipment_type': 'B2B',
#             })
#             formset = cosigneeFormSet(queryset=consignee.objects.none(), prefix='form2')
#             print('printing formset else part',formset)
        
        
#         return render(request, 'b2bportal/newbooking.html', {
#             'booking': booking_id,
#             'formset': formset,
#             'form': form,
#             'company': company
          
#         })


def newconsignee(request):
    cosigneeFormSet = modelformset_factory(consignee,
                                           fields=('contact_person', 'address1', 'address2', 'country', 'mobile_number1', 'city'), extra=0)
    # consignee=Booking.objects.get(id=booking_id).consignee.all()

    if request.method == "POST":
        form = ShipmentBookingForm(request.POST, queryset=consignee.objects.all())
        if form.is_valid():
            form_save = form.save(commit=False)
        else:
            print(form.non_form_errors())
        return HttpResponse(status=204)
        pass
    else:
        formset = cosigneeFormSet(
            queryset=consignee.objects.none(), prefix='form2')

    return render(request, 'b2bportal/consigneehtmx.html', {'formset': formset, 'consignee_data': 'none'})

@login_required(login_url="/premium-login/")
def estimated_delivery(request):
     
    form=EDDNewForm()
    
    if request.GET.get('id',None) != None:
        org_country=request.POST.get("data")
        city_list=city.objects.filter(country_id=org_country)
        city_data=""
        for row in city_list:
            city_data+="<option value='{}'>{}</option>".format(row.id,row.name)
        return HttpResponse(city_data) 

    if request.POST:
        print(request.POST)
        form=EDDNewForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
           
            message="<h5>Your oder will be delivered in 6 days. Estimate Delivery date is 14 May 2023 </h5>"
        else:
            message="<h3 class='text-red'>Invalid Form Post </h3>"
        return HttpResponse(message) 

    if request.htmx:
        base_template="b2bportal/_partial.html"
    else:
        base_template="b2bportal/base.html"

    if request.POST:
        form=EDDNewForm(request.POST)
  

    context={
         
         'form':form,
         'base_template':base_template
    }
    return render(request, 'b2bportal/edd_new.html',context=context)

def edd(request):
 
    countries = country.objects.all()
    form=EDDForm()
    
    if request.htmx:
        base_template="b2bportal/_partial.html"
    else:
        base_template="b2bportal/base.html"

    if request.POST:
        form=EDDForm(request.POST)
        
    
    context={
         'countries': countries,
         'form':form,
         'base_template':base_template
    }
    return render(request, 'b2bportal/edd.html',context=context)


def checkCities(request):
     
    if request.is_ajax and request.method == "GET":
        # get the nick name from the client side.
        country_code = request.GET.get("country_code", None)       
        oCountry = country.objects.filter(code = country_code).first() 
        print(oCountry)
        cities = city.objects.filter(country__id=oCountry.id)
        return JsonResponse({"cities": list(cities.values('code', 'name'))}, status=200)

def saveEDD(request):
    print("Rashmi")
    if request.is_ajax and request.method == "POST":
        _Date = request.POST.get("from_date", None)
        _Time = request.POST.get("time", None)
        _OriginCountry = request.POST.get("KSA", None)
        _OriginCity = request.POST.get("OriginCity", None)
        _DestinationCountry = request.POST.get("KSA", None)
        _DestinationCity = request.POST.get("DestinationCity", None)
        _ServiceType = request.POST.get("ServiceType", None)
        _ProductType = request.POST.get("ProductType", None)
        _Weight = request.POST.get("Weight", None)
        originCountry = country.objects.filter(code=_OriginCountry).first()
        print('origin country',originCountry)
        originCity = city.objects.filter(code=_OriginCity).first()
        
        destinationCountry = country.objects.filter(
            code=_DestinationCountry).first()
        destinationCity = city.objects.filter(code=_DestinationCity).first()

        data = EstimatedDeliveryDuration(date=_Date, time=_Time, originCountry=originCountry.id, originCity=originCity.id, destinationCountry=destinationCountry.id,
                                         destinationCity=destinationCity.id, serviceType=_ServiceType, productType=_ProductType, weight=_Weight, createdDate=datetime.now())
        data.save()
        return JsonResponse({"responseJSON": "success"}, status=200)
@login_required(login_url="/premium-login/") 
def Enquiries(request):
    if request.htmx:
        base_template="b2bportal/_partial.html"
    else:
        base_template="b2bportal/base.html"
    form =EnquiryModuleForm()
    form=ComplaintsModuleForm()
    context={}
    if request.method =='POST':

        if  'EnqSubmit' in request.POST:
            form =EnquiryModuleForm (request.POST)
            #form.add_error();
            if form.is_valid():
                #Adding Validation                  
                print("here No Error")
                form.save()
                mail_subject = 'Help Request Submitted.'

                message = render_to_string('b2bportal/Enquiry_Email_template.html', {
                    'Name': form.cleaned_data.get('Name'),
                    'Email': form.cleaned_data.get('Email'),
                    'PhoneNo': form.cleaned_data.get('PhoneNo'),
                    'Details': form.cleaned_data.get('Details'),
                })
           
            # #Send WhatsApp message
            # cleanedPhNo =  str(form.cleaned_data.get('PhoneNo'))
            # # Convert string to list
            # listOfChars = list(cleanedPhNo)
            # # Replace first character in list with 'X'
            # listOfChars[0] = '+966'
            # # Convert the list to string
            # cleanedPhNo = ''.join(listOfChars)            
            # print(cleanedPhNo)
            # kit.sendwhatmsg_instantly(cleanedPhNo, "Your enquire has been registered successfully, Our Customer Service team will contact you shortly"
            #                 , 10, tab_close=True)


                #to_email = form.cleaned_data.get('Email')            
                #to_email = "rashmi.ranjan@naqel.com.sa"
                to_email = "Inquiries@naqel.com.sa"
                send_html_mail(mail_subject, message, [to_email])
                message="<h4 class='text-success'>Your Enquiry has been registered successfully, Our Customer Service team will contact you shortly</h4>"
                return HttpResponse(message) 
              
            else:
                message="<h4 class='text-danger'>Please enter valid data for enquiry</h4>"
                return HttpResponse(message) 
      
        elif  'CAFsubmit' in request.POST:
            form =ComplaintsModuleForm (request.POST)
            if form.is_valid():
                form.save()
                mail_subject = 'CAF is Submitted.'
                message = render_to_string('b2bportal/Complaint_Email_template.html', {
                    'Name': form.cleaned_data.get('Name'),
                    'Email': form.cleaned_data.get('Email'),
                    'PhoneNo': form.cleaned_data.get('PhoneNo'),
                    'Reason': form.cleaned_data.get('Reason'),
                    'Details': form.cleaned_data.get('Details'),
                })
                #to_email =form.cleaned_data.get('Email')
                #o_email = "rashmi.ranjan@naqel.com.sa"
                to_email = "Inquiries@naqel.com.sa"
                send_html_mail(mail_subject, message, [to_email])
                   
                message="<h4 class='text-success'>Your complaint has been registered successfully, Our Complaint team will contact you shortly</h4>"
                return HttpResponse(message) 
            else:
                message="<h4 class='text-danger'>Please enter valid data for Complaint</h4>"
                return HttpResponse(message) 
    else:
        context={
            'form': form,
            'csdata': CScontact.objects.all(),
            'keydata': KeyAccountContact.objects.all(),
            'base_template':base_template
        }
    return render(request, 'b2bportal/Enquiries.html',context=context)

    


def Register(request):

    if request.method == 'POST':
        form = B2BRegisterationForm(request.POST)
        print("Rashmi")
        countrytext = request.POST.get('Country')
        print(countrytext)
        if form.is_valid():
            print("here")
            form.save()
            mail_subject = 'B2B Client Request.'

            message = render_to_string('b2bportal/Registeration_Email_template.html', {
                'ComName': form.cleaned_data.get('ComName'),
                'CustomerName': form.cleaned_data.get('CustomerName'),
                'IndType': form.cleaned_data.get('IndType'),
                'MoNumber': form.cleaned_data.get('MoNumber'),
                'Email': form.cleaned_data.get('Email'),
                'Address': form.cleaned_data.get('Address'),
                'City': form.cleaned_data.get('City'),
                'Country': form.cleaned_data.get('Country'),
            })
            #to_email = form.cleaned_data.get('Email')
            #to_email = "rashmi.ranjan@naqel.com.sa"
            to_email = "Inquiries@naqel.com.sa"
            send_html_mail(mail_subject, message, [to_email])
            return TemplateResponse(request, 'b2bportal/Registeration_submission.html', {'message':
                                                                                       'You have successfully registered, Our customer services will contact you shortly', })

    else:
        print("Rashmi")
        form = B2BRegisterationForm()
    return render(request, 'b2bportal/Registeration.html',{'form': form})

def add_to_favourite(request):
    form = ShipmentBookingForm(request.POST)
    booking_id=request.POST.get("booking_id")
    booking=Booking.objects.get(pk=booking_id)
    fav=request.POST.get("pintoservice")
    if fav=="1":
        booking.is_fav=True
    else:
        booking.is_fav=False
    booking.save()
    print(booking_id) 
    return HttpResponse(status=204)
     

def favouritebooking(request):
    company=GetCurrentCompany(request)
    fav_list=Booking.objects.filter(company_profile=company,is_fav=True).order_by('-id')
    return render(request,'b2bportal/favouritebooking.html',context={"records":fav_list})


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


def b2blogin(request):
    """Renders the Service page."""

    if request.method == 'POST':
        form = B2BLoginForm(request.POST)
        print(request.POST.get('username'))
        user = NaqelUser.objects.filter(
            email=request.POST.get('username')).first()
        print("User", user)
        if user is not None:
            username = user.username
            password = request.POST.get('password')
            user = authenticate(username=user.username, password=password)

            if user is not None:
                login(request, user)
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
    return render(request, 'b2bportal/login.html', {'form': form})


def convertJSONDate(json_date):
    
    if json_date ==None:
        return ""
    if json_date =="THE VALUE NOT AVAILABLE":
        return ""
    json_date = str(json_date).replace("T"," ")
    if str(json_date).find(".") != -1 :
        json_date = json_date[:-14]
        print(json_date)
    json_date = str(json_date).replace("Before ","")
    dtobject = datetime.datetime.strptime(json_date, '%Y-%m-%d %H:%M:%S')
    return dtobject    

def convertStrDate(str_date):
    format = "%m/%d/%Y %I:%M:%S %p"
    jdate = datetime.datetime.strptime(str_date, format)
    return jdate


def tracking(request):
    
    if request.htmx:
        base_template="b2bportal/_partial.html"
    else:
        base_template="b2bportal/base.html"

    company=GetCurrentCompany(request)

    current_tracking=Booking.objects.filter(company_profile=company).order_by('-id')[:5]
    waybills_items = []
    if request.method == 'POST':
        form = TrackingForm(request.POST)
        if 'submit_waybill' in request.POST :
            waybills= request.POST.get('varwaybill', None).replace('\n', ',')
            print('Hist Track : '+waybills)
        else:            
            waybills = request.POST.get('waybills', None).replace('\n', ',')
        
        print("LL",waybills)

        waybill_list = []
        try:
            for x in waybills.split(','):
                # print(x)
                if x.isalnum() or x != "" or x:
                    # print(x)
                    # print("bywaybill")
                    waybill_list.append(x)
                    # print(waybill_list)
                elif x != "" or x:
                    # print("here")
                    waybill_list.append(int(x))
                    # print(waybill_list)

        except:
            pass
        
        
        try:
            for wb in waybill_list:
                task = {"MobileNo": "0553200062", "OriginID": 501, "DestinationID": 501,
                        "Reference": wb, "AppVersion": "test", "WaybillNo": wb}
                
                Webapilink = 'https://customerappapi.naqelksa.com/api/Api/Track/TraceByWaybillNoRefNo'
                resp = requests.post(Webapilink, json=task)
                data = resp.json()
                #print(data)

                #print(data["TrackingResult"][0]["PickupDate"])
                waybillno = data["TrackingResult"][0]["WaybillNo"]
                print("result",waybillno)

                PickupDate = convertJSONDate(
                    data["TrackingResult"][0]["PickupDate"])
                print(PickupDate)
             
                PiecesCount = data["TrackingResult"][0]["PiecesCount"]
                destination = data["TrackingResult"][0]["DestName"]
                current_status = data["TrackingResult"][0]["Activity"]
                destinationar = data["TrackingResult"][0]["DestFName"]
                current_statusar = data["TrackingResult"][0]["ActivityFName"]
                EventCode = data["TrackingResult"][0]["EventCode"]
                if data["TrackingResult"][0]["ExpectedDeliveryDate"] != None:
                    expectedDeliveryDate = convertJSONDate(data["TrackingResult"][0]["ExpectedDeliveryDate"])
                else:
                    expectedDeliveryDate = "None"
                is_pickedup = False
                is_intransit = False
                is_delevered = False
                
                tracking = Tracking(waybillno=waybillno, pickupdate=PickupDate,
                                    piececount=PiecesCount, destination=destination, currentstatus=current_status,
                                    destinationar=destinationar, currentstatusar=current_statusar, eventCode=EventCode,expected_delivery=expectedDeliveryDate)

               
                tracking_details = []
                tracking_eventcode = []
                records = data["TrackingResult"]
                for track in records:
                    waybill_id = track["WaybillNo"]
                    actiondate = convertStrDate(track["Date"])
                    actiontime = convertStrDate(track["Date"])

                    location = track["StationName"]
                    locationAr = track["StationFName"]
                    description = track["Activity"]
                    descriptionAr = track["ActivityFName"]
                    EventCode_details = track["EventCode"]

                    trackingDetails = TrackingDetails(actiondate=actiondate,
                                                      actiontime=actiontime,
                                                      location=location,
                                                      locationAr=locationAr,
                                                      description=description,
                                                      descriptionAr=descriptionAr,
                                                      eventCode=EventCode_details)
                    tracking_details.append(trackingDetails)
                    tracking_eventcode.append(trackingDetails.eventCode)
                    for item in tracking_eventcode:
                        if item == 1 or item == 0:
                            is_pickedup = True
                        elif item == 7:
                            is_delevered = True
                           
                        else:
                            is_intransit = True
                            is_pickedup = True
                    dates_and_items = {}
                    for detail in tracking_details:
                        current_key = detail.actiondate.date()  # the item's date
                        dates_and_items.setdefault(
                            current_key, []).append(detail)

                waybills_items.append(
                    {'waybill': tracking, 'dates_and_items': dates_and_items, 'isdeleverd': is_delevered,
                     'is_pickup': is_pickedup, 'is_intransit': is_intransit})
            book=Booking.objects.all()         
            wbTrack=CustomerWaybill.objects.filter(booking_no=book.booking_no,booking_id=book.id).first() 

        except:
            pass

        #print(waybills_items)  
        #print('CSK : ' + waybills)        
        # print(form.waybills)
        # form.data["waybills"] = '12345678'
        return render(request, 'b2bportal/Tracking.html', {
                'tracking': waybills_items,
                'form': form,
                'title': 'Shipment Tracking',
                'records':current_tracking,
                'base_template':base_template

            })
    else:

        form = TrackingForm()

        return render(request, 'b2bportal/Tracking.html', {
            'tracking': waybills_items,
            'form': form,
            'title': 'Shipment Tracking',
            'records':current_tracking,
            'base_template':base_template
        })    
     
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
 
from django.views.generic.base import TemplateView
class B2BPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = "/reset/done/"

def password_reset_request(request):
    error=None
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = NaqelUser.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "b2bportal/password/password_reset_email.txt"
                    c = {
                        "email":user.email,
                        'domain':'127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                return redirect ("/password_reset/done/")
            else:
                error='Enter a valid registered Email'
               
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="b2bportal/password/password_reset.html", context={"form":password_reset_form,"error":error})
 
def reset_password(request):
    Error=None
    if request.method =='POST':
        
        form =PasswordResetCustomForm (request.POST)
        print("Rashmi here")
        if form.is_valid():
            
            to_email=form.cleaned_data.get('Email')

            myuser=NaqelUser.objects.filter(email=to_email)
            if myuser.count() > 0:
                mail_subject = 'Help Request Submitted.'

                message = render_to_string('b2bportal/password_reset_done.html', {
                    'Name': form.cleaned_data.get('Name'),
                    'Email': form.cleaned_data.get('Email'),
                    'PhoneNo': form.cleaned_data.get('PhoneNo'),
                    'Details': form.cleaned_data.get('Details'),
                })
                send_html_mail(mail_subject, message, [to_email])
                return TemplateResponse(request, 'b2bportal/password_reset_done.html', {'message':
                                                                                       'Your Passord generated suceessfully', })

            else:
                Error="User not found or Email Not registered "
        else:
            Error="Please enter registered email "

    else:
        form=PasswordResetCustomForm

    context={
        'form': form,
        'error':Error,
       

    }
    return render(request, 'b2bportal/reset_password.html',context=context)

@login_required(login_url="/premium-login/")
def clientreport(request):   
    
    if request.htmx:
        base_template="b2bportal/_partial.html"
    else:
        base_template="b2bportal/base.html"

    if request.method == 'POST':
        print("Entering")
        form = ClientForm(request.POST)        
        fromdate=request.POST.get("from_date")
        todate=request.POST.get("to_date")

        task = {"StartDate": fromdate, "EndDate": todate, "ClientID": "9020077"}
        data=None
        try:
                print(fromdate)
                print(todate)
                task = {"StartDate": fromdate, "EndDate": todate, "ClientID": "9020077"}
                Webapilink = 'http://212.107.118.74:81/b2b/daily-recap-get'
                resp = requests.post(Webapilink, data=task)
                data = resp.json()
                 
                #print('response data',data)
        except:
            pass
        
        template_name="DailyRecap.ods"

        if "btnpdf" in request.POST:
            filename="DailyRecap.pdf"
        elif "btnexcel":
            filename="DailyRecap.xlsx"

        if data == None:
            context={}
        else:
            context={
                "data_list":data["Result"]
            }


        #return generate_report_document(request,template_name,filename,context)
        form = ClientForm()
        return render(request, 'b2bportal/clientreport.html', {
            'form': form,
            'title': 'Client Report',
            'base_template':base_template
        })
 
    else:

        form = ClientForm()
        return render(request, 'b2bportal/clientreport.html', {
            'form': form,
            'title': 'Client Report',
            'base_template':base_template
        })

@login_required(login_url="/premium-login/")
def invoice(request):
    records=None
    form=InvoiceForm()
    if request.method == 'POST':
        print('Post method','')
        form = InvoiceForm(request.POST)
        print(form)
        if form.is_valid():
            company=GetCurrentCompany(request)
            ClientID=company.client_id
            print('ClientID',ClientID)
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            task = {"StartDate": from_date, "EndDate": to_date, "ClientID": ClientID}
       
        try:    
                print(from_date)
                print(to_date)
                task = {"StartDate": from_date, "EndDate": to_date, "ClientID": ClientID}
                Webapilink = 'http://212.107.118.74:81/b2b/invoice-get'
                resp = requests.post(Webapilink, data=task)
                records = resp.json()["Result"]
                print(records) 
        except:
            pass

            
    return render(request, 'b2bportal/invoice.html', {
        'form':form,
        'records':records
})


def basecompanyprofile(request):
    company=GetCurrentCompany(request)
    # default_shipper=CompanyProfile.objects.all()
    

    return render(request, 'b2bportal/profile.html', {        
        'company':company,
})