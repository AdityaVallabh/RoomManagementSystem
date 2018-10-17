from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Hotel

# Create your views here.

def search(request):
    locations = Hotel.objects.all().values_list('location', flat=True).distinct()
    if not request.GET.get('location', 'none') == 'none':
        location = request.GET['location']
        hotels = Hotel.objects.filter(location=location)

        return render(request, 'hotels/search.html', {'hotels': hotels, 'locations': locations, 'location': location})

    return render(request, 'hotels/search.html', {'locations': locations})

class HotelList(ListView):
    model = Hotel
    context_object_name = 'hotels_list'
    template_name='hotels/hotel_list.html'

class HotelDetail(DetailView):
    model = Hotel
    template_name='hotels/hotel_detail.html'


