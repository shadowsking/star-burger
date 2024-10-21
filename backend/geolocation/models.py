from django.db import models
from star_burger import settings

from .geocode import fetch_coordinates


class GeoLocationQuerySet(models.QuerySet):
    def get_or_create_location(self, address):
        location = self.filter(address=address)
        if location:
            return location[0]

        coordinates = fetch_coordinates(
            apikey=settings.GEO_API_KEY,
            address=address
        )
        if not coordinates:
            return

        return self.get_or_create(
            address=address,
            **coordinates
        )


class GeoLocation(models.Model):
    address = models.CharField(
        max_length=255,
        verbose_name='адрес',
        unique=True
    )
    lat = models.FloatField(
        verbose_name='широта',
        null=True,
        blank=True,
    )
    lon = models.FloatField(
        verbose_name='долгота',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        'дата создания',
        auto_now_add=True,
        db_index=True
    )

    objects = GeoLocationQuerySet.as_manager()

    class Meta:
        verbose_name = 'геолокация'
        verbose_name_plural = 'геолокации'

    def __str__(self):
        return self.address

    @property
    def coordinates(self):
        return self.lat, self.lon
