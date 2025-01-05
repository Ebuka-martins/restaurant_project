from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

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