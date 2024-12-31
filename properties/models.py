from django.db import models

class HotelSummary(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE)
    property_id = models.IntegerField()
    summary = models.TextField()

    def __str__(self):
        return f"Summary for {self.hotel.hotel_name}"

class HotelReview(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE)
    property_id = models.IntegerField()
    rating = models.FloatField()
    review = models.TextField()

    def __str__(self):
        return f"Review for {self.hotel.hotel_name}"

class Hotel(models.Model):
    # This represents your existing hotels table
    id = models.IntegerField(primary_key=True)
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
    description = models.TextField(null=True, blank=True)

    class Meta:
        managed = False  # Since this table already exists
        db_table = 'hotels'  # Specify the exact table name