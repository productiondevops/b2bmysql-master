from core.models import *

def getdata(request):
  #add filter
    data = client.objects.all()
    # csdata = CScontact.objects.all()

    return{'data':data, }