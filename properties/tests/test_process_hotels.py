from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from unittest.mock import patch, MagicMock
from io import StringIO

import requests
from properties.models import Hotel, HotelSummary, HotelReview
from properties.management.commands.process_hotels import Command

class CommandTestCase(TestCase):
    databases = []  # Tell Django not to use any databases for these tests
    
    def setUp(self):
        self.command = Command()
        self.command.stdout = StringIO()
        
        # Create a mock hotel instance
        self.mock_hotel = MagicMock()
        self.mock_hotel.hotel_id = 1
        self.mock_hotel.hotel_name = "Test Hotel"
        self.mock_hotel.hotel_address = "123 Test St"
        self.mock_hotel.price = 100.0
        self.mock_hotel.rating = 4.5
        self.mock_hotel.room_type = "Standard"
        self.mock_hotel.lat = 1.0
        self.mock_hotel.lng = 1.0

    @patch('properties.management.commands.process_hotels.requests.post')
    def test_check_model_status(self, mock_post):
        """Test check_model_status method."""
        # Test successful response
        mock_post.return_value = MagicMock(status_code=200)
        self.assertTrue(self.command.check_model_status())
        
        # Test failed response
        mock_post.return_value = MagicMock(status_code=404)
        self.assertFalse(self.command.check_model_status())
        
        # Test exception case
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")
        self.assertFalse(self.command.check_model_status())  # Expect False since exception is caught


    @patch('properties.management.commands.process_hotels.requests.post')
    @patch('properties.management.commands.process_hotels.time.sleep')
    def test_pull_llama_model(self, mock_sleep, mock_post):
        """Test pull_llama_model method."""
        # Mock stdout.write directly without recursion
        self.command.stdout.write = MagicMock()

        # Test successful pulls
        mock_post.side_effect = [
            MagicMock(status_code=200),
            MagicMock(status_code=200)
        ]
        self.assertTrue(self.command.pull_llama_model())

        # Test failed pull (properly simulate failure with an exception)
        mock_post.side_effect = requests.exceptions.RequestException("Pull failed")
        self.assertFalse(self.command.pull_llama_model())  # Ensure the method returns False on failure



    @patch('properties.management.commands.process_hotels.requests.post')
    def test_generate_ollama_content(self, mock_post):
        """Test generate_ollama_content method."""
        mock_response = MagicMock(
            status_code=200,
            json=lambda: {'response': 'Generated content'}
        )
        mock_post.return_value = mock_response
        result = self.command.generate_ollama_content("Test prompt")
        self.assertEqual(result, 'Generated content')

    @patch('properties.models.HotelSummary.objects.create')
    @patch('properties.models.HotelReview.objects.create')
    @patch.object(Command, 'generate_ollama_content')
    def test_process_hotel(self, mock_generate, mock_review_create, mock_summary_create):
        """Test process_hotel method."""
        mock_generate.side_effect = [
            "Test Title",
            "Test Description",
            "Test Summary",
            "Test Review\nRating: 4.5/5"
        ]
        
        # Test processing the mock hotel
        self.command.process_hotel(self.mock_hotel)
        
        # Ensure the create methods were called
        mock_summary_create.assert_called_once()
        mock_review_create.assert_called_once()

    @patch('properties.models.Hotel.objects')
    @patch.object(Command, 'check_model_status')
    @patch.object(Command, 'pull_llama_model')
    @patch.object(Command, 'process_hotel')
    def test_handle(self, mock_process_hotel, mock_pull_model, mock_check_status, mock_hotel_objects):
        """Test handle method."""
        # Set up mocks
        mock_queryset = MagicMock()
        mock_queryset.__iter__.return_value = iter([self.mock_hotel])  # Ensure the queryset is iterable
        mock_queryset.count.return_value = 1  # Ensure the count is correct
        mock_hotel_objects.all.return_value = mock_queryset  # Return the mock queryset when calling all()
        
        mock_check_status.return_value = True  # Mock that the model status check is successful
        mock_pull_model.return_value = True  # Mock that pulling the model is successful
        
        # Test command execution
        self.command.handle()
        
    def test_error_handling(self):
        """Test error handling in process_hotel."""
        with patch.object(Command, 'generate_ollama_content') as mock_generate:
            mock_generate.side_effect = Exception("Test error")
            self.command.process_hotel(self.mock_hotel)
            self.assertIn("Error processing hotel", self.command.stdout.getvalue())