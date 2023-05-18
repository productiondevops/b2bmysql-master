from dal import autocomplete
from .models import *
from django.db.models import Q

class CountryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        qs = country.objects.all()
        if self.q:
             qs = qs.filter(Q(name__icontains=self.q))
        return qs



class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        qs = city.objects.none()
        country_var=self.forwarded.get('country',None)
        if country_var:
            qs = city.objects.all()
            qs=qs.filter(country=country_var)
        if self.q:
             qs = qs.filter(Q(name__icontains=self.q))
        return qs