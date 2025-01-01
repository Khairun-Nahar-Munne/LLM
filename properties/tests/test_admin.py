from unittest.mock import MagicMock, patch
from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from properties.admin import HotelAdmin, HotelSummaryAdmin, HotelReviewAdmin
from properties.models import Hotel, HotelSummary, HotelReview

class AdminTests(TestCase):
    def setUp(self):
        self.site = AdminSite()

        # Mock the Hotel object
        self.hotel = MagicMock(spec=Hotel)
        self.hotel.city_id = 1
        self.hotel.hotel_name = "Test Hotel"
        self.hotel.hotel_address = "123 Test St"
        self.hotel.hotel_img = "test.jpg"
        self.hotel.price = 100.0

    @patch('properties.admin.Hotel')
    def test_hotel_admin_display(self, MockHotel):
        MockHotel.objects = MagicMock()
        hotel_admin = HotelAdmin(MockHotel, self.site)
        self.assertIn('hotel_name', hotel_admin.list_display)
        self.assertIn('description', hotel_admin.list_display)

    @patch('properties.admin.Hotel')
    def test_hotel_admin_filters(self, MockHotel):
        MockHotel.objects = MagicMock()
        hotel_admin = HotelAdmin(MockHotel, self.site)
        self.assertIn('city_id', hotel_admin.list_filter)
        self.assertIn('room_type', hotel_admin.list_filter)

    @patch('properties.admin.HotelSummary')
    def test_summary_admin_display(self, MockHotelSummary):
        MockHotelSummary.objects = MagicMock()
        summary_admin = HotelSummaryAdmin(MockHotelSummary, self.site)
        self.assertIn('summary', summary_admin.list_display)

    @patch('properties.admin.HotelReview')
    def test_review_admin_display(self, MockHotelReview):
        MockHotelReview.objects = MagicMock()
        review_admin = HotelReviewAdmin(MockHotelReview, self.site)
        self.assertIn('rating', review_admin.list_display)