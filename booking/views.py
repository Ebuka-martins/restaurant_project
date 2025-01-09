from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Avg, Count
from django.db.models.functions import ExtractMonth
from datetime import datetime, timedelta
from .models import Booking, Table, BookingAnalytics, CustomerInsights, RevenueMetrics, CustomerFeedback
from .forms import BookingForm
from .utils import send_booking_confirmation, send_cancellation_confirmation
from django.conf import settings

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
                
                # Update analytics
                today = datetime.now().date()
                analytics, created = BookingAnalytics.objects.get_or_create(
                    date=today,
                    defaults={
                        'total_bookings': 1,
                        'total_guests': booking.number_of_guests,
                        'cancelled_bookings': 0
                    }
                )
                if not created:
                    analytics.total_bookings += 1
                    analytics.total_guests += booking.number_of_guests
                    analytics.save()

                # Update revenue metrics (assuming average spend per guest)
                avg_spend_per_guest = 50  # Adjust this value based on your restaurant's average
                revenue, created = RevenueMetrics.objects.get_or_create(
                    date=today,
                    defaults={
                        'total_revenue': booking.number_of_guests * avg_spend_per_guest,
                        'avg_revenue_per_booking': avg_spend_per_guest
                    }
                )
                if not created:
                    revenue.total_revenue += booking.number_of_guests * avg_spend_per_guest
                    revenue.avg_revenue_per_booking = (
                        revenue.total_revenue / analytics.total_bookings
                    )
                    revenue.save()

                send_booking_confirmation(booking)
                messages.success(request, 'Booking confirmed! Check your email for details.')
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

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.user != request.user:
        return HttpResponseForbidden("You don't have permission to cancel this booking.")
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()

        # Update analytics for cancellation
        today = datetime.now().date()
        analytics, created = BookingAnalytics.objects.get_or_create(
            date=today,
            defaults={
                'total_bookings': 0,
                'total_guests': 0,
                'cancelled_bookings': 1
            }
        )
        if not created:
            analytics.cancelled_bookings += 1
            analytics.save()

        send_cancellation_confirmation(booking)
        messages.success(request, 'Booking cancelled successfully!')
        return redirect('booking_list')
        
    return render(request, 'booking/cancel_booking.html', {'booking': booking})

@login_required
def delete_all_bookings(request):
    if request.method == 'POST':
        # Delete all bookings for the current user
        Booking.objects.filter(user=request.user).delete()
        messages.success(request, 'All bookings have been successfully deleted.')
        return redirect('booking_list')
    return render(request, 'booking/delete_all_bookings.html')

class AnalyticsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'booking/analytics_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)  # Last 30 days

        # Get booking analytics with detailed debug logging
        analytics = BookingAnalytics.objects.filter(
            date__range=[start_date, end_date]
        ).aggregate(
            total_bookings=Sum('total_bookings'),
            total_guests=Sum('total_guests'),
            cancelled_bookings=Sum('cancelled_bookings')
        )

        # Get revenue metrics
        revenue = RevenueMetrics.objects.filter(
            date__range=[start_date, end_date]
        ).aggregate(
            total_revenue=Sum('total_revenue'),
            avg_revenue_per_booking=Avg('avg_revenue_per_booking')
        )

        # Get customer feedback
        feedback = CustomerFeedback.objects.filter(
            created_at__date__range=[start_date, end_date]
        ).aggregate(
            avg_rating=Avg('rating'),
            total_reviews=Count('id')
        )

        # Calculate additional metrics
        if analytics['total_bookings']:
            cancellation_rate = (
                (analytics['cancelled_bookings'] or 0) / analytics['total_bookings']
            ) * 100
        else:
            cancellation_rate = 0

        context.update({
            'analytics': analytics,
            'revenue': revenue,
            'feedback': feedback,
            'cancellation_rate': cancellation_rate,
            'date_range': {
                'start': start_date,
                'end': end_date
            },
            'debug': settings.DEBUG
        })
        return context

def menu_view(request):
    menu_items = MenuItem.objects.filter(available=True).order_by('category', 'name')
    categories = MenuItem.CATEGORY_CHOICES
    
    context = {
        'categories': categories,
        'menu_items': menu_items,
    }
    return render(request, 'booking/menu.html', context)
