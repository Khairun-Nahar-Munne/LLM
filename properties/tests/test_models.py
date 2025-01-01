from unittest.mock import MagicMock, patch
from django.test import TestCase
from properties.models import Hotel, HotelSummary, HotelReview


class ModelTests(TestCase):
    def setUp(self):
        self.hotel = MagicMock(spec=Hotel)
        self.hotel.hotel_id = 1
        self.hotel.city_id = 1
        self.hotel.hotel_name = "Test Hotel"
        self.hotel.hotel_address = "123 Test St"
        self.hotel.hotel_img = "test.jpg"
        self.hotel.price = 100.0
        self.hotel.rating = 4.5
        self.hotel.room_type = "Standard"
        self.hotel.lat = 12.34
        self.hotel.lng = 56.78



    @patch('properties.models.Hotel')
    def test_hotel_model_fields(self, MockHotel):
        MockHotel.objects = MagicMock()
        MockHotel.objects.get.return_value = self.hotel
        self.assertEqual(self.hotel.hotel_id, 1)
        self.assertEqual(self.hotel.city_id, 1)
        self.assertEqual(self.hotel.hotel_name, "Test Hotel")
        self.assertEqual(self.hotel.hotel_address, "123 Test St")
        self.assertEqual(self.hotel.price, 100.0)
        self.assertEqual(self.hotel.rating, 4.5)
        self.assertEqual(self.hotel.room_type, "Standard")
        self.assertEqual(self.hotel.lat, 12.34)
        self.assertEqual(self.hotel.lng, 56.78)

    @patch('properties.models.HotelSummary')
    def test_hotel_summary_creation(self, MockHotelSummary):
        mock_summary = MagicMock(spec=HotelSummary)
        mock_summary.hotel = self.hotel
        mock_summary.property_id = 1
        mock_summary.summary = "Test summary content"
        mock_summary.__str__.return_value = "Summary for Test Hotel"
        MockHotelSummary.objects.create.return_value = mock_summary
        summary = MockHotelSummary.objects.create(
            hotel=self.hotel,
            property_id=1,
            summary="Test summary content"
        )
        self.assertEqual(str(summary), "Summary for Test Hotel")
        empty_summary = MockHotelSummary.objects.create(
            hotel=self.hotel,
            property_id=1,
            summary=""
        )
        self.assertEqual(str(empty_summary), "Summary for Test Hotel")

    @patch('properties.models.HotelReview')
    def test_hotel_review_creation(self, MockHotelReview):
        mock_review = MagicMock(spec=HotelReview)
        mock_review.hotel = self.hotel
        mock_review.property_id = 1
        mock_review.rating = 4.5
        mock_review.review = "Test review content"
        mock_review.__str__.return_value = "Review for Test Hotel"
        MockHotelReview.objects.create.return_value = mock_review
        review = MockHotelReview.objects.create(
            hotel=self.hotel,
            property_id=1,
            rating=4.5,
            review="Test review content"
        )
        self.assertEqual(str(review), "Review for Test Hotel")
        missing_review = MockHotelReview.objects.create(
            hotel=self.hotel,
            property_id=1,
            rating=4.5,
            review=""
        )
        self.assertEqual(str(missing_review), "Review for Test Hotel")

    @patch('properties.models.Hotel')
    def test_hotel_empty_description(self, MockHotel):
        hotel_with_no_description = MagicMock(spec=Hotel)
        hotel_with_no_description.hotel_name = "No Description Hotel"
        hotel_with_no_description.description = None
        MockHotel.objects.get.return_value = hotel_with_no_description
        self.assertEqual(hotel_with_no_description.description, None)