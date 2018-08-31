from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Hotel

# Create your views here.

class HotelList(ListView):
    model = Hotel
    context_object_name = 'hotels_list'
    template_name='hotels/hotel_list.html'

class HotelDetail(DetailView):
    model = Hotel
    template_name='hotels/hotel_detail.html'