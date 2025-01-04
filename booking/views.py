from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Booking, Table
from .forms import BookingForm
from django.contrib import messages

# Create your views here.
@login_required
def make_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            
            # Find available table
            tables = Table.objects.filter(capacity__gte=booking.number_of_guests)
            available_table = None
            
            for table in tables:
                if not Booking.objects.filter(
                    table=table,
                    booking_date=booking.booking_date,
                    booking_time=booking.booking_time
                ).exists():
                    available_table = table
                    break
            
            if available_table:
                booking.table = available_table
                booking.save()
                messages.success(request, 'Booking confirmed!')
                return redirect('booking_list')
            else:
                messages.error(request, 'No tables available for this time.')
    else:
        form = BookingForm()
    
    return render(request, 'booking/make_booking.html', {'form': form})

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user).order_by('booking_date', 'booking_time')
    return render(request, 'booking/booking_list.html', {'bookings': bookings})


