from django.db import models

class HotelContent(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"Content for {self.hotel.hotel_name}"

class HotelSummary(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE)
    summary = models.TextField()

    def __str__(self):
        return f"Summary for {self.hotel.hotel_name}"

class HotelReview(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE)
    rating = models.FloatField()
    review = models.TextField()

    def __str__(self):
        return f"Review for {self.hotel.hotel_name}"

class Hotel(models.Model):
    # This represents your existing hotels table
    hotel_id = models.IntegerField()
    city_id = models.IntegerField()
    hotel_name = models.CharField(max_length=255)
    hotel_address = models.CharField(max_length=255)
    hotel_img = models.CharField(max_length=255)
    price = models.FloatField(null=True)
    rating = models.FloatField(null=True)
    room_type = models.CharField(max_length=255, null=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    class Meta:
        managed = False  # Since this table already exists
        db_table = 'hotels'  # Specify the exact table name