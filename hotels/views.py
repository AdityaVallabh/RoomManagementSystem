from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Hotel, Room ,Booking
from .forms import BookingForm, ContactForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from RoomManagementSystem.emails import BOOKING_EMAIL, CONTACT_EMAIL
from accounts.models import User
from django.core.mail import EmailMessage
from django.utils import timezone

# Create your views here.

def search(request):
    locations = Hotel.objects.all().values_list('location', flat=True).distinct()
    if not request.GET.get('location', 'none') == 'none':
        location = request.GET['location']
        hotels = Hotel.objects.filter(location=location)
        return render(request, 'hotels/search.html', {'hotels': hotels, 'locations': locations, 'location': location})

    return render(request, 'hotels/search.html', {'locations': locations})


def emailView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            location = form.cleaned_data['location']
            hotel_name = form.cleaned_data['hotel_name']
            hotel_email = form.cleaned_data['hotel_email']
            email = form.cleaned_data['email']
            contact = form.cleaned_data['contact']
            subject = '[YOYO] ' + name + ' wants to add ' + hotel_name + ' (' + location + ')'
            message = CONTACT_EMAIL % (hotel_name,location,hotel_email,name,email,contact)
            admin_email = User.objects.get(pk=1).email
            success = False
            try:
                email = EmailMessage(subject, message, to=[admin_email])
                email.send()
                success = True
            except Exception as e:
                print("Unable to send email to (%s)\n%s" % (admin_email, e))
            return  render(request, "hotels/email.html", {'success': success})
    return render(request, "hotels/email.html", {'form': form})


@method_decorator(login_required, name='dispatch')
class BookingCreate(CreateView):
    form_class = BookingForm
    template_name = 'hotels/booking.html'
    room = None

    # def send_email(self, transaction):
    #     try:
    #         subject = "Invoice for Transaction %d" % transaction.id
    #         body = BOOKING_EMAIL % (transaction.from_user.first_name, transaction.from_user.last_name, transaction.id, transaction.from_user.username, transaction.to_user.username, transaction.amount, transaction.time, transaction.success)
    #         email = EmailMessage(subject, body, to=[transaction.from_user.email])
    #         email.send()
    #     except:
    #         print("Unable to send email (%s)" % transaction.from_user.email)

    def get_initial(self):
        if self.request.GET.get('room_id') and Room.objects.filter(id=self.request.GET['room_id']):
            return { 'room': Room.objects.get(id=self.request.GET['room_id'])}
    
    def get_context_data(self, **kwargs):
        ctx = super(BookingCreate, self).get_context_data(**kwargs)
        ctx['price'] = Room.objects.get(id=self.request.GET['room_id']).cost
        return ctx
    
    def check_availability(self, room, checkin, checkout, num_rooms):
        if checkout <= checkin:
            return 'Check-Out can not be before or equal to Check-In', False
        bookings = Booking.objects.filter(room=room)
        occupied = 0
        for booking in bookings:
            if booking.begin_time < checkout and booking.end_time > checkin:
                occupied += booking.num_rooms
        available = room.maximum - occupied
        return ('Available', True) if num_rooms <= available else ('Rooms not available on given dates', False)


    def form_valid(self, form):
        booking = form.save(commit=False)
        booking.customer = self.request.user
        booking.amount = booking.num_rooms * booking.room.cost * (booking.end_time - booking.begin_time).days
        message, success = self.check_availability(booking.room, booking.begin_time, booking.end_time, booking.num_rooms)
        if(not success):
            return render(self.request, 'hotels/booking.html', {'room': booking.room, 'message': message})
        # transaction = Transaction()
        # transaction, success = transaction.make_transaction(from_user=self.request.user.userprofile, to_user=booking.room, amount=booking.fee, reason="Book Booking")
        # if success:
        #     booking.transaction_id = transaction
        #     booking.save()
        # else:
        #     print('Transaction %d failed' % transaction.id)
        # self.send_email(transaction)
        booking.save()
        return redirect('index')


class HotelList(ListView):
    model = Hotel
    context_object_name = 'hotels_list'
    template_name = 'hotels/hotel_list.html'

class HotelDetail(DetailView):
    model = Hotel
    template_name = 'hotels/hotel_detail.html'

class RoomList(ListView):
    model = Room
    context_object_name = 'rooms_list'
    template_name = 'hotels/room_list.html'

    queryset = Room.objects.all()

    def get_queryset(self):
        return Room.objects.filter(hotel=self.kwargs.get('hotel_pk'))

class RoomDetail(DetailView):
    model = Room
    template_name='hotels/room_detail.html'

class BookingList(ListView):
    template_name = 'hotels/booking-list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Booking.objects.all()
        elif self.request.user.is_authenticated:
            if self.request.user.is_customer:
                return Booking.objects.filter(customer=self.request.user)

class BookingDetail(DetailView):
    model = Booking
    template_name = 'hotels/booking-details.html'

    def post(self, request, *args, **kwargs):
        if request.POST.get('rating'):
            user_rating = int(request.POST.get('rating'))
            self.object = super(BookingDetail, self).get_object()
            hotel = self.object.room.hotel
            if self.object.user_rating == 0:
                hotel.rating = (hotel.rating * hotel.num_rating + user_rating)/(hotel.num_rating + 1)
                hotel.num_rating += 1
            else:
                hotel.rating = (hotel.rating * hotel.num_rating - self.object.user_rating + user_rating)/(hotel.num_rating)
            hotel.save()
            self.object.user_rating = user_rating
            self.object.save()
            print(self.object.user_rating)
            return redirect('index')
        return self.get(request)
            