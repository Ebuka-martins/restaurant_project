from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from .models import (
    Table,
    Booking,
    BookingAnalytics,
    CustomerFeedback,
    RevenueMetrics,
    CustomerInsights
)

class BookingListTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test table
        self.table = Table.objects.create(
            table_number=1,
            capacity=4
        )
        
        # Create test booking
        self.booking = Booking.objects.create(
            user=self.user,
            table=self.table,
            booking_date=timezone.now().date(),
            booking_time=timezone.now().time(),
            number_of_guests=2,
            status='confirmed'
        )
        
        self.client = Client()
        
    def test_booking_list_view_authenticated(self):
        """Test booking list view for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('booking_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/booking_list.html')
        
        # Check if booking details are in the response
        self.assertContains(response, str(self.table.table_number))
        self.assertContains(response, str(self.booking.number_of_guests))
        self.assertContains(response, 'confirmed')
        
        # Check context
        bookings = response.context['bookings']
        self.assertEqual(len(bookings), 1)
        self.assertEqual(bookings[0], self.booking)
        
    def test_booking_list_view_unauthenticated(self):
        """Test booking list view redirects for unauthenticated user"""
        response = self.client.get(reverse('booking_list'))
        login_url = reverse('login')
        self.assertRedirects(response, f'{login_url}?next=/')

class CreateBookingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.table = Table.objects.create(
            table_number=1,
            capacity=4
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        
    def test_make_booking_successful(self):
        """Test successful booking creation"""
        booking_data = {
            'booking_date': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
            'booking_time': '19:00',
            'number_of_guests': 2
        }
        
        response = self.client.post(reverse('make_booking'), booking_data)
        
        # Check redirection to booking list
        self.assertRedirects(response, reverse('booking_list'))
        
        # Verify booking was created
        booking = Booking.objects.first()
        self.assertIsNotNone(booking)
        self.assertEqual(booking.number_of_guests, 2)
        self.assertEqual(booking.status, 'confirmed')
        
        # Check analytics were updated
        analytics = BookingAnalytics.objects.first()
        self.assertIsNotNone(analytics)
        self.assertEqual(analytics.total_bookings, 1)
        self.assertEqual(analytics.total_guests, 2)

class CancelBookingTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.table = Table.objects.create(
            table_number=1,
            capacity=4
        )
        self.booking = Booking.objects.create(
            user=self.user,
            table=self.table,
            booking_date=timezone.now().date(),
            booking_time=timezone.now().time(),
            number_of_guests=2,
            status='confirmed'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        
    def test_cancel_booking_successful(self):
        """Test successful booking cancellation"""
        response = self.client.post(reverse('cancel_booking', args=[self.booking.id]))
        
        # Check redirection
        self.assertRedirects(response, reverse('booking_list'))
        
        # Verify booking status changed
        booking = Booking.objects.get(id=self.booking.id)
        self.assertEqual(booking.status, 'cancelled')
        
        # Check analytics
        analytics = BookingAnalytics.objects.first()
        self.assertEqual(analytics.cancelled_bookings, 1)

class DeleteAllBookingsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.table = Table.objects.create(
            table_number=1,
            capacity=4
        )
        self.booking = Booking.objects.create(
            user=self.user,
            table=self.table,
            booking_date=timezone.now().date(),
            booking_time=timezone.now().time(),
            number_of_guests=2,
            status='confirmed'
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
    
    def test_delete_all_bookings(self):
        """Test deleting all bookings"""
        response = self.client.post(reverse('delete_all_bookings'))
        
        # Check redirection
        self.assertRedirects(response, reverse('booking_list'))
        
        # Verify all bookings were deleted
        self.assertEqual(Booking.objects.filter(user=self.user).count(), 0)
        
        # Check analytics were updated
        analytics = BookingAnalytics.objects.first()
        self.assertEqual(analytics.total_bookings, 0)

class AnalyticsDashboardTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='staffuser',
            password='testpass123',
            is_staff=True
        )
        self.client = Client()
        self.client.login(username='staffuser', password='testpass123')
        
        # Create test data
        self.table = Table.objects.create(table_number=1, capacity=4)
        BookingAnalytics.objects.create(
            date=timezone.now().date(),
            total_bookings=10,
            total_guests=30,
            cancelled_bookings=2
        )
        
        RevenueMetrics.objects.create(
            date=timezone.now().date(),
            total_revenue=Decimal('500.00'),
            avg_revenue_per_booking=Decimal('50.00')
        )
        
    def test_analytics_dashboard_view(self):
        """Test analytics dashboard displays correct data"""
        response = self.client.get(reverse('analytics_dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/analytics_dashboard.html')
        
        context = response.context
        self.assertIn('analytics', context)
        self.assertIn('revenue', context)