# Updated properties/cli.py
from django.core.management.base import BaseCommand
import requests
import json
import time
from properties.models import Hotel, HotelSummary, HotelReview

class Command(BaseCommand):
    help = 'Process hotel data using Ollama'
    
    MODEL_NAME = "llama3.2"  # Updated to use llama3.2

    def pull_llama_model(self):
        """Pull the Llama3.2 model if not already present"""
        url = "http://ollama:11434/api/pull"
        data = {
            "name": self.MODEL_NAME
        }
        
        self.stdout.write(f"Pulling {self.MODEL_NAME} model... This might take several minutes...")
        
        try:
            response = requests.post(url, json=data)
            while response.status_code == 200:
                self.stdout.write(".", ending='')
                time.sleep(2)
                # Check if model is ready
                check_url = "http://ollama:11434/api/show"
                check_response = requests.post(check_url, json={"name": self.MODEL_NAME})
                if check_response.status_code == 200:
                    self.stdout.write(f"\n{self.MODEL_NAME} model successfully pulled!")
                    return True
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'\nError pulling model: {str(e)}'))
            return False

    def check_model_status(self):
        """Check if the Llama3.2 model is available"""
        url = "http://ollama:11434/api/show"
        data = {
            "name": self.MODEL_NAME
        }
        
        try:
            response = requests.post(url, json=data)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def handle(self, *args, **kwargs):
        # First, check if model is available
        self.stdout.write(f"Checking {self.MODEL_NAME} model status...")
        
        if not self.check_model_status():
            self.stdout.write(f"{self.MODEL_NAME} model not found. Pulling model...")
            if not self.pull_llama_model():
                self.stdout.write(self.style.ERROR(f'Failed to pull {self.MODEL_NAME} model. Exiting...'))
                return
        else:
            self.stdout.write(self.style.SUCCESS(f"{self.MODEL_NAME} model is already available!"))

        # Get first 10 hotels
        hotels = Hotel.objects.all()[:10] 
        total_hotels = hotels.count()
        
        self.stdout.write(f"Processing {total_hotels} hotels...")
        
        for index, hotel in enumerate(hotels, 1):
            self.stdout.write(f"Processing hotel {index}/{total_hotels}: {hotel.hotel_name}")
            self.process_hotel(hotel)

    def generate_ollama_content(self, prompt):
        """Generate content using Ollama API with Llama3.2"""
        url = "http://ollama:11434/api/generate"
        data = {
            "model": self.MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                return response.json()['response']
            self.stdout.write(self.style.WARNING(f"Failed to generate content. Status code: {response.status_code}"))
            return None
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Error generating content: {str(e)}"))
            return None

    def process_hotel(self, hotel):
        try:
            hotel_info = f"""
            Hotel Name: {hotel.hotel_name}
            Address: {hotel.hotel_address}
            Price: ${hotel.price}
            Rating: {hotel.rating}
            Room Type: {hotel.room_type}
            Location: Lat {hotel.lat}, Lng {hotel.lng}
            """
            self.stdout.write("Generating summary...")
            summary_prompt = f"Generate a concise summary of this hotel's key features:\n{hotel_info}"
            summary_response = self.generate_ollama_content(summary_prompt)
            
            if summary_response:
                HotelSummary.objects.create(
                    hotel=hotel,
                    summary=summary_response,
                    property_id=hotel.hotel_id
                )
                self.stdout.write(self.style.SUCCESS("Summary generated successfully"))

            # Generate review and rating
            self.stdout.write("Generating review and rating...")
            review_prompt = f"Based on this hotel information, generate a detailed review and suggest a rating out of 5:\n{hotel_info}"
            review_response = self.generate_ollama_content(review_prompt)
            
            if review_response:
                try:
                    rating = float(review_response.split('Rating:', 1)[1].split('/')[0].strip())
                except:
                    rating = 4.0  # Default rating if parsing fails
                    
                HotelReview.objects.create(
                    hotel=hotel,
                    rating=rating,
                    review=review_response,
                    property_id=hotel.hotel_id
                )

                self.stdout.write(self.style.SUCCESS("Review and rating generated successfully"))
            
            self.stdout.write("Generating title...")
            title_prompt = f"Create a title using this hotel name and just give one line: {hotel.hotel_name}"
            title = self.generate_ollama_content(title_prompt).strip()
            
            # Update the hotels table directly
            if title:
                hotel.hotel_name = title
                hotel.save(update_fields=["hotel_name"])
                self.stdout.write(self.style.SUCCESS(f"Updated hotel {hotel.id}: {title}"))

            self.stdout.write("Generating hotel description...")
            description_prompt = f"Generate a detailed hotel description at least two lines about these details:\n{hotel_info}"
            description_response = self.generate_ollama_content(description_prompt).strip()
            
            if description_response:
                hotel.description = description_response
                hotel.save(update_fields=["description"])
                self.stdout.write(self.style.SUCCESS("Description generated and saved successfully"))
          


        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error processing hotel {hotel.hotel_name}: {str(e)}"))