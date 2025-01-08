from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Table(models.Model):
    table_number = models.IntegerField(unique=True)
    capacity = models.IntegerField()

    def __str__(self):
        return f"Table {self.table_number} (Capacity: {self.capacity})"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    number_of_guests = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled'),
        ],
        default='confirmed'
    )

    class Meta:
        unique_together = ['table', 'booking_date', 'booking_time']
    
    def __str__(self):
        return f"Booking for {self.user.username} - Table {self.table.table_number} - Status: {self.status}"

class BookingAnalytics(models.Model):
    date = models.DateField(unique=True)
    total_bookings = models.IntegerField(default=0)
    confirmed_bookings = models.IntegerField(default=0)
    cancelled_bookings = models.IntegerField(default=0)
    total_guests = models.IntegerField(default=0)
    avg_guests_per_booking = models.FloatField(default=0)
    
    class Meta:
        verbose_name_plural = "Booking Analytics"

    def __str__(self):
        return f"Analytics for {self.date}"

class CustomerFeedback(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 rating
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for booking {self.booking.id} - Rating: {self.rating}"

class RevenueMetrics(models.Model):
    date = models.DateField(unique=True)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    avg_revenue_per_booking = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    avg_revenue_per_guest = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name_plural = "Revenue Metrics"

    def __str__(self):
        return f"Revenue metrics for {self.date}"

class CustomerInsights(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_bookings = models.IntegerField(default=0)
    cancelled_bookings = models.IntegerField(default=0)
    avg_group_size = models.FloatField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_visit = models.DateField(null=True, blank=True)
    preferred_dining_time = models.TimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Insights for {self.user.username}"