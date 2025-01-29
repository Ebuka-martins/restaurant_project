from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Avg, Count
from django.db.models.functions import ExtractMonth
from django.core.paginator import Paginator
from itertools import groupby
from operator import attrgetter
from datetime import datetime, timedelta
from .models import (
    Booking,
    Table,
    BookingAnalytics,
    CustomerInsights,
    RevenueMetrics,
    CustomerFeedback,
    MenuItem
)
from .forms import BookingForm
from .utils import send_booking_confirmation, send_cancellation_confirmation
from django.conf import settings


# Booking-related views
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
    # Get all bookings for the user, ordered by date and time
    booking_list = Booking.objects.filter(user=request.user).order_by('booking_date', 'booking_time')
    
    # Create a paginator object with 5 bookings per page
    paginator = Paginator(booking_list, 5) 
    
    # Get the page number from the request
    page_number = request.GET.get('page')
    
    # Get the Page object for the current page
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'booking/booking_list.html', {
        'bookings': page_obj,  
        'page_obj': page_obj,  
    })

@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Check if the booking is confirmed (can only edit confirmed bookings)
    if booking.status != 'confirmed':
        messages.error(request, 'Only confirmed bookings can be edited.')
        return redirect('booking_list')
    
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            new_booking = form.save(commit=False)
            
            # Find available table
            tables = Table.objects.filter(capacity__gte=new_booking.number_of_guests)
            available_table = None

            for table in tables:
                existing_bookings = Booking.objects.filter(
                    table=table,
                    booking_date=new_booking.booking_date,
                    booking_time=new_booking.booking_time,
                    status='confirmed'
                ).exclude(id=booking_id)  # Exclude current booking
                
                if not existing_bookings.exists():
                    available_table = table
                    break

            if available_table:
                new_booking.table = available_table
                new_booking.save()
                messages.success(request, 'Booking updated successfully!')
                return redirect('booking_list')
            else:
                messages.error(request, 'No tables available for this time.')
    else:
        form = BookingForm(instance=booking)
    
    return render(request, 'booking/edit_booking.html', {
        'form': form,
        'booking': booking
    })

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
        user = request.user

        # Retrieve all user bookings
        user_bookings = Booking.objects.filter(user=user)
        booking_ids = list(user_bookings.values_list('id', flat=True))

        # Delete related customer feedback
        CustomerFeedback.objects.filter(booking__id__in=booking_ids).delete()

        # Delete user bookings
        user_bookings.delete()

        # Recalculate customer insights for the user
        insights, _ = CustomerInsights.objects.get_or_create(user=user)
        insights.total_bookings = 0
        insights.cancelled_bookings = 0
        insights.avg_group_size = 0
        insights.total_spent = 0
        insights.last_visit = None
        insights.preferred_dining_time = None
        insights.save()

        # Update BookingAnalytics
        for analytics in BookingAnalytics.objects.all():
            date = analytics.date
            bookings = Booking.objects.filter(booking_date=date)

            analytics.total_bookings = bookings.count()
            analytics.confirmed_bookings = bookings.filter(status='confirmed').count()
            analytics.cancelled_bookings = bookings.filter(status='cancelled').count()
            analytics.total_guests = bookings.aggregate(total=Sum('number_of_guests'))['total'] or 0
            analytics.avg_guests_per_booking = (
                analytics.total_guests / analytics.total_bookings if analytics.total_bookings > 0 else 0
            )
            analytics.save()

        # Update RevenueMetrics
        for revenue in RevenueMetrics.objects.all():
            date = revenue.date
            bookings = Booking.objects.filter(booking_date=date)

            total_revenue = bookings.aggregate(
                total=Sum('number_of_guests') * 50  # Replace with actual revenue calculation
            )['total'] or 0

            total_guests = bookings.aggregate(total=Sum('number_of_guests'))['total'] or 0

            revenue.total_revenue = total_revenue
            revenue.avg_revenue_per_booking = (
                total_revenue / bookings.count() if bookings.exists() else 0
            )
            revenue.avg_revenue_per_guest = (
                total_revenue / total_guests if total_guests > 0 else 0
            )
            revenue.save()

        # Confirmation message
        messages.success(request, 'All bookings and analytics recalculated successfully.')
        return redirect('booking_list')

    return render(request, 'booking/delete_all_bookings.html')


# Analytics dashboard
class AnalyticsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'booking/analytics_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)  # Last 30 days

        # Get booking analytics
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
    # Get menu items and sort them by category
    menu_items = MenuItem.objects.filter(available=True).order_by('category', 'name')
    
    # Create a dictionary with category as key and list of items as value
    menu_by_category = {}
    # Convert QuerySet to list to prevent iterator exhaustion
    menu_items_list = list(menu_items)
    
    for category, items in groupby(menu_items_list, key=attrgetter('category')):
        menu_by_category[category] = list(items)
    
    # Debug print
    print("Categories:", menu_by_category.keys())
    print("Total items:", len(menu_items_list))
    
    context = {
        'menu_by_category': menu_by_category,
        'menu_items': menu_items,  # Keep the original queryset for debugging
        'categories': MenuItem.CATEGORY_CHOICES
    }
    return render(request, 'booking/menu.html', context)


# Static pages
def about_view(request):
    """View for the About page"""
    return render(request, 'booking/about.html')
