from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Avg, Count, Sum
from django.utils import timezone
from datetime import datetime
from .models import Booking, BookingAnalytics, CustomerInsights, RevenueMetrics

# Analytics functions
def update_booking_analytics(date=None):
    if not date:
        date = timezone.now().date()
    
    bookings = Booking.objects.filter(booking_date=date)
    analytics, created = BookingAnalytics.objects.get_or_create(date=date)
    analytics.total_bookings = bookings.count()
    analytics.confirmed_bookings = bookings.filter(status='confirmed').count()
    analytics.cancelled_bookings = bookings.filter(status='cancelled').count()
    analytics.total_guests = bookings.aggregate(Sum('number_of_guests'))['number_of_guests__sum'] or 0
    
    if analytics.total_bookings > 0:
        analytics.avg_guests_per_booking = analytics.total_guests / analytics.total_bookings
    
    analytics.save()

def update_customer_insights(user):
    insights, created = CustomerInsights.objects.get_or_create(user=user)
    user_bookings = Booking.objects.filter(user=user)
    
    insights.total_bookings = user_bookings.count()
    insights.cancelled_bookings = user_bookings.filter(status='cancelled').count()
    insights.avg_group_size = user_bookings.aggregate(Avg('number_of_guests'))['number_of_guests__avg'] or 0
    
    if user_bookings.exists():
        insights.last_visit = user_bookings.latest('booking_date').booking_date
        preferred_time = user_bookings.values('booking_time')\
            .annotate(count=Count('booking_time'))\
            .order_by('-count').first()
        if preferred_time:
            insights.preferred_dining_time = preferred_time['booking_time']
    
    insights.save()

def update_revenue_metrics(date=None):
    if not date:
        date = timezone.now().date()
    
    bookings = Booking.objects.filter(booking_date=date, status='confirmed')
    AVG_SPEND_PER_GUEST = 30  # Adjust this based on actual data
    
    metrics, created = RevenueMetrics.objects.get_or_create(date=date)
    total_guests = bookings.aggregate(Sum('number_of_guests'))['number_of_guests__sum'] or 0
    metrics.total_revenue = total_guests * AVG_SPEND_PER_GUEST
    
    if bookings.count() > 0:
        metrics.avg_revenue_per_booking = metrics.total_revenue / bookings.count()
        metrics.avg_revenue_per_guest = AVG_SPEND_PER_GUEST
    
    metrics.save()

# Email functions
def send_booking_confirmation(booking):
    subject = f'Booking Confirmation - {booking.booking_date}'
    context = {
        'booking': booking,
        'restaurant_name': 'Your Restaurant Name',
        'restaurant_address': 'Your Restaurant Address',
        'restaurant_phone': 'Your Restaurant Phone',
    }
    
    html_message = render_to_string('booking/email/booking_confirmation.html', context)
    plain_message = render_to_string('booking/email/booking_confirmation.txt', context)
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email='your-restaurant@example.com',
        recipient_list=[booking.user.email],
        html_message=html_message,
    )
    
    # Update analytics after sending confirmation email
    update_booking_analytics(date=booking.booking_date)
    update_customer_insights(user=booking.user)
    update_revenue_metrics(date=booking.booking_date)

def send_cancellation_confirmation(booking):
    subject = f'Booking Cancellation - {booking.booking_date}'
    context = {
        'booking': booking,
        'restaurant_name': 'Your Restaurant Name',
    }
    
    html_message = render_to_string('booking/email/booking_cancellation.html', context)
    plain_message = render_to_string('booking/email/booking_cancellation.txt', context)
    
    send_mail(
        subject=subject,
        message=plain_message,
        from_email='your-restaurant@example.com',
        recipient_list=[booking.user.email],
        html_message=html_message,
    )
    
    # Update analytics after sending cancellation email
    update_booking_analytics(date=booking.booking_date)
    update_customer_insights(user=booking.user)
