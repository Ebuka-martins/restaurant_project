from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Avg
from django.db.models.functions import ExtractMonth
from datetime import datetime, timedelta
from .models import Booking, Table, BookingAnalytics, CustomerInsights, RevenueMetrics, CustomerFeedback
from .forms import BookingForm
from .utils import send_booking_confirmation, send_cancellation_confirmation  # Import email utility functions

# Make a booking
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
                    booking_time=booking.booking_time,
                    status='confirmed'
                ).exists():
                    available_table = table
                    break

            if available_table:
                booking.table = available_table
                booking.save()
                send_booking_confirmation(booking)  # Send confirmation email
                messages.success(request, 'Booking confirmed! Check your email for details.')
                return redirect('booking_list')
            else:
                messages.error(request, 'No tables available for this time.')
    else:
        form = BookingForm()

    return render(request, 'booking/make_booking.html', {'form': form})

# List bookings
@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user).order_by('booking_date', 'booking_time')
    return render(request, 'booking/booking_list.html', {'bookings': bookings})

# Cancel a booking
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Check if the booking belongs to the user
    if booking.user != request.user:
        return HttpResponseForbidden("You don't have permission to cancel this booking.")
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        send_cancellation_confirmation(booking)
        messages.success(request, 'Booking cancelled successfully! Check your email for confirmation.')
        return redirect('booking_list')
        
    return render(request, 'booking/cancel_booking.html', {'booking': booking})

def menu_view(request):
    menu_items = MenuItem.objects.filter(available=True).order_by('category', 'name')
    categories = MenuItem.CATEGORY_CHOICES
    
    context = {
        'categories': categories,
        'menu_items': menu_items,
    }
    return render(request, 'booking/menu.html', context)

# Analytics Dashboard View
class AnalyticsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'booking/analytics_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)

        # Get booking analytics
        analytics = BookingAnalytics.objects.filter(
            date__range=[start_date, end_date]
        ).aggregate(
            total_bookings=Sum('total_bookings'),
            total_guests=Sum('total_guests'),
            cancelled_bookings=Sum('cancelled_bookings')
        )
        print("Analytics:", analytics)  # Debugging

        # Get revenue metrics
        revenue = RevenueMetrics.objects.filter(
            date__range=[start_date, end_date]
        ).aggregate(
            total_revenue=Sum('total_revenue'),
            avg_revenue_per_booking=Avg('avg_revenue_per_booking')
        )
        print("Revenue:", revenue)  # Debugging

        # Get customer feedback summary
        feedback = CustomerFeedback.objects.filter(
            created_at__date__range=[start_date, end_date]
        ).aggregate(
            avg_rating=Avg('rating')
        )
        print("Feedback:", feedback)

        context.update({
            'analytics': analytics,
            'revenue': revenue,
            'feedback': feedback,
            'date_range': {
                'start': start_date,
                'end': end_date
            }
        })
        return context
