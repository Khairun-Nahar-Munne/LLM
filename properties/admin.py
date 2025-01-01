# admin.py
from django.contrib import admin
from .models import Hotel, HotelSummary, HotelReview

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('id','hotel_name', 'description')
    list_filter = ('city_id', 'room_type')
    search_fields = ('hotel_name', 'hotel_address')
    readonly_fields = ('id', 'hotel_id')  # Since these are primary/foreign keys
    list_per_page = 25

    fieldsets = (
        ('Basic Information', {
            'fields': ('hotel_name', 'hotel_address', 'hotel_img')
        }),
        ('Details', {
            'fields': ('price', 'rating', 'room_type', 'description')
        }),
        ('Location', {
            'fields': ('city_id', 'lat', 'lng')
        }),
        ('System Fields', {
            'fields': ('id', 'hotel_id'),
            'classes': ('collapse',)
        })
    )

@admin.register(HotelSummary)
class HotelSummaryAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'summary')
    search_fields = ('hotel__hotel_name', 'summary')

@admin.register(HotelReview)
class HotelReviewAdmin(admin.ModelAdmin):
    list_display = ('property_id', 'rating', 'review')
    list_filter = ('rating',)
    search_fields = ('hotel__hotel_name', 'review')