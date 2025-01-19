from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Booking
from .utils import (
    update_booking_analytics,
    update_customer_insights,
    update_revenue_metrics,
)


@receiver(post_save, sender=Booking)
def booking_saved_handler(sender, instance, created, **kwargs):
    """
    Signal handler for when a booking is created or updated.
    """
    # Update analytics for the booking date
    update_booking_analytics(instance.booking_date)

    # Update customer insights
    update_customer_insights(instance.user)

    # Update revenue metrics
    update_revenue_metrics(instance.booking_date)


@receiver(post_delete, sender=Booking)
def booking_deleted_handler(sender, instance, **kwargs):
    """
    Signal handler for when a booking is deleted.
    """
    # Update analytics for the booking date
    update_booking_analytics(instance.booking_date)

    # Update customer insights
    update_customer_insights(instance.user)

    # Update revenue metrics
    update_revenue_metrics(instance.booking_date)
